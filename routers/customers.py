from fastapi import APIRouter, Depends, HTTPException

from sqlite.database import get_db
from sqlalchemy.orm import Session

from sqlite import schemas
from sqlite.models import User
from sqlite.crud import customers
from sqlite.crud import users

from utils_auth import user_should_be_customer, get_current_user


router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(user_should_be_customer)],
    responses={
        403: {"model": schemas.Custom403ErrorResponse},
        404: {"model": schemas.Custom404ErrorResponse},
    },
)


@router.post("/increase", response_model=schemas.User)
async def increase_watts_consumed(
    watts_consumed: schemas.CustomerWattBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return customers.increase_watts_consumed(
        watts_consumed=watts_consumed, db_user=current_user, db=db
    )


@router.get("/bill}")
async def generate_bill(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return customers.calculate_customer_bill(db_user=current_user, db=db)
