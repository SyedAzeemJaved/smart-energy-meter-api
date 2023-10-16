from sqlalchemy.orm import Session

from sqlite import models, schemas
from utils import return_per_unit_cost_depending_on_time


# Customers
def get_customer_by_id(cux_id: int, db: Session):
    return db.query(models.Customer).filter(models.Customer.id == cux_id).first()


def get_customer_by_nic_number(cux_nic: str, db: Session):
    return (
        db.query(models.Customer).filter(models.Customer.nic_number == cux_nic).first()
    )


def top_up_account(
    account_balance: schemas.CustomerAccountBalanceBase,
    db_user: models.User,
    db: Session,
):
    previous_account_balance = db_user.customer.account_balance_in_rupees
    new_account_balance = (
        previous_account_balance + account_balance.account_balance_in_rupees
    )

    db_user.customer.account_balance_in_rupees = new_account_balance
    if new_account_balance > 0:
        db_user.customer.should_get_service = True
    db.commit()
    return db_user


def increase_units_consumed(units_consumed: float, db_user: models.User, db: Session):
    previous_units_consumed = db_user.customer.units_consumed
    current_reading_units_consumed = units_consumed

    total_units_consumed_after_this_reading = (
        previous_units_consumed + current_reading_units_consumed
    )

    previous_account_balance = db_user.customer.account_balance_in_rupees
    new_account_balance = previous_account_balance - (
        current_reading_units_consumed * float(return_per_unit_cost_depending_on_time())
    )

    db_user.customer.units_consumed = total_units_consumed_after_this_reading
    db_user.customer.account_balance_in_rupees = new_account_balance

    if new_account_balance <= 0:
        db_user.customer.should_get_service = False

    db.commit()
    return db_user
