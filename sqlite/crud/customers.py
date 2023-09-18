from sqlalchemy.orm import Session

from sqlite import models, schemas
from utils import secret


# Customers
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
    db.refresh(db_user)
    return db_user


def increase_watts_consumed(
    watts_consumed: schemas.CustomerWattBase, db_user: models.User, db: Session
):
    previous_watts_consumed = db_user.customer.watts_consumed
    current_reading_watts_consumed = watts_consumed.watts_consumed

    total_watts_consumed_after_this_reading = (
        previous_watts_consumed + current_reading_watts_consumed
    )

    current_reading_units_consumed = current_reading_watts_consumed / 1000

    previous_account_balance = db_user.customer.account_balance_in_rupees
    new_account_balance = previous_account_balance - (
        current_reading_units_consumed * float(secret.PER_UNIT_COST_IN_RUPEES)
    )

    db_user.customer.watts_consumed = total_watts_consumed_after_this_reading
    db_user.customer.account_balance_in_rupees = new_account_balance

    if new_account_balance <= 0:
        db_user.customer.should_get_service = False

    db.commit()
    db.refresh(db_user)
    return db_user


def calculate_customer_bill(db_user: models.User, db: Session):
    units_consumed = db_user.customer.watts_consumed / 1000
    return f"You have used {units_consumed} units, please pay {units_consumed * float(secret.PER_UNIT_COST_IN_RUPEES)} rupees to continue using our service."
