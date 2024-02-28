from fastapi import APIRouter, Depends, HTTPException
from sqlite.crud import users, customers

from sqlite.database import get_db
from sqlalchemy.orm import Session
from sqlite import schemas

from utils import (
    are_object_to_edit_and_other_object_same_by_email,
    are_object_to_edit_and_other_object_same_by_nic,
)
from utils_auth import user_should_be_admin

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(user_should_be_admin)],
    responses={
        403: {"model": schemas.Custom403ErrorResponse},
        404: {"model": schemas.Custom404ErrorResponse},
    },
)


@router.get("/all", response_model=list[schemas.User])
async def get_everyone(db: Session = Depends(get_db)):
    return users.get_everyone(db=db)


@router.get("/all/admins", response_model=list[schemas.UserAdmin])
async def get_all_admins(db: Session = Depends(get_db)):
    return users.get_admins(db=db)


@router.get("/all/customers", response_model=list[schemas.User])
async def get_all_customers(db: Session = Depends(get_db)):
    return users.get_customers(db=db)


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/admin", response_model=schemas.UserAdmin)
async def set_admin_user(user: schemas.UserAdminCreate, db: Session = Depends(get_db)):
    db_user = users.get_user_by_email(user_email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=403, detail="User already exists")
    return users.create_admin_user(user=user, db=db)


@router.post("/customer", response_model=schemas.User)
async def set_customer_user(
    user: schemas.UserCustomerCreate, db: Session = Depends(get_db)
):
    db_user = users.get_user_by_email(user_email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=403, detail="User already exists")
    db_cux = customers.get_customer_by_nic_number(
        cux_nic=user.customer.nic_number, db=db
    )
    if db_cux:
        raise HTTPException(status_code=403, detail="Customer already exists")
    return users.create_customer_user(user=user, db=db)


@router.put(
    "/{user_id}/admin",
    response_model=schemas.UserAdmin,
)
async def update_admin_user(
    user_id: int, user: schemas.UserUpdateWithoutCustomer, db: Session = Depends(get_db)
):
    db_user = users.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    other_object = users.get_user_by_email(user_email=user.email, db=db)
    if other_object:
        if not are_object_to_edit_and_other_object_same_by_email(
            obj_to_edit=db_user, other_object_with_same_email=other_object
        ):
            raise HTTPException(
                status_code=403, detail="User with same email already exists"
            )
    return users.update_admin_user(user=user, db_user=db_user, db=db)


@router.put(
    "/{user_id}/customer",
    response_model=schemas.User,
)
async def update_customer_user(
    user_id: int, user: schemas.UserUpdateWithCustomer, db: Session = Depends(get_db)
):
    db_user = users.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    other_object = users.get_user_by_email(user_email=user.email, db=db)
    if other_object:
        if not are_object_to_edit_and_other_object_same_by_email(
            obj_to_edit=db_user, other_object_with_same_email=other_object
        ):
            raise HTTPException(
                status_code=403, detail="User with same email already exists"
            )
    db_cux = customers.get_customer_by_id(cux_id=db_user.customer.id, db=db)
    if db_cux is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    other_object = customers.get_customer_by_nic_number(
        cux_nic=user.customer.nic_number, db=db
    )
    if other_object:
        if not are_object_to_edit_and_other_object_same_by_nic(
            obj_to_edit=db_cux, other_object_with_same_nic=other_object
        ):
            raise HTTPException(
                status_code=403, detail="Customer with same nic already exists"
            )
    return users.update_customer_user(user=user, db_user=db_user, db=db)


@router.delete(
    "/{user_id}",
    response_model=schemas.CustomSuccessResponse,
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users.delete_user(db_user=db_user, db=db)


@router.post("/customer/topup/{user_id}", response_model=schemas.User)
async def top_up_customer_account(
    user_id: int,
    topup_amount: schemas.CustomerTopupAccountBalanceBase,
    db: Session = Depends(get_db),
):
    db_user = users.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return customers.top_up_account(
        topup_amount=topup_amount, db_user=db_user, db=db
    )
