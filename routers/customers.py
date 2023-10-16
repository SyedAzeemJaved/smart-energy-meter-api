from fastapi import APIRouter, Depends

from sqlite.database import get_db
from sqlalchemy.orm import Session

from sqlite import schemas
from sqlite.models import User
from sqlite.crud import customers

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


@router.get("/me", response_model=schemas.User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/should-get-service", response_model=bool)
async def should_get_service(current_user: User = Depends(get_current_user)):
    return current_user.customer.should_get_service


@router.post("/increase", response_model=schemas.User)
async def increase_units_consumed(
    readings: schemas.CustomerReadingBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.customer.update_previous_readings(readings=readings)
    return customers.increase_units_consumed(
        units_consumed=readings.units_consumed, db_user=current_user, db=db
    )
