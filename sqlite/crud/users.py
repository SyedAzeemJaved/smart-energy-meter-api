from sqlalchemy.orm import Session, joinedload

from sqlite import models, schemas
from utils import return_datetime_in_proper_format, get_password_hash


# Users
def get_everyone(db: Session):
    return db.query(models.User).options(joinedload(models.User.customer)).all()


def get_admins(db: Session):
    return (
        db.query(models.User)
        .filter(models.User.is_admin == True)
        .options(joinedload(models.User.customer))
        .all()
    )


def get_customers(db: Session):
    return (
        db.query(models.User)
        .filter(models.User.is_admin == False)
        .options(joinedload(models.User.customer))
        .all()
    )


def get_user_by_id(user_id: int, db: Session):
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .options(joinedload(models.User.customer))
        .first()
    )


def get_user_by_email(user_email: str, db: Session):
    return (
        db.query(models.User)
        .filter(models.User.email == user_email)
        .options(joinedload(models.User.customer))
        .first()
    )


def create_admin_user(user: schemas.UserAdminCreate, db: Session):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.__dict__, is_admin=True)
    db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def create_customer_user(user: schemas.UserCustomerCreate, db: Session):
    db_user = models.User(
        name=user.name, email=user.email, password=get_password_hash(user.password)
    )
    # Create Customer instance
    db_user.customer = models.Customer(
        user_id=db_user.id,
        nic_number=user.customer.nic_number,
        units_consumed=0.0,
        account_balance_in_rupees=0.0,
        should_get_service=False,
        previous_voltage_reading=0.0,
        previous_current_reading=0.0,
    )
    db.add(db_user)
    
    db.commit()
    return db_user


def update_admin_user(
    user: schemas.UserUpdateWithoutCustomer, db_user: models.User, db: Session
):
    db_user.update(user)
    
    db.commit()
    return db_user


def update_customer_user(
    user: schemas.UserUpdateWithCustomer,
    db_user: models.User,
    db: Session,
):
    db_user.update(user)
    db_user.customer.update(user.customer)
    db_user.customer.updated_at = return_datetime_in_proper_format()
    
    db.commit()
    return db_user


def delete_user(db_user: models.User, db: Session):
    db.delete(db_user)
    
    db.commit()
    return {"detail": "Deleted successfully"}
