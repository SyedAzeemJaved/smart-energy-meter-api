from sqlalchemy.orm import Session

from sqlite.crud.users import get_user_by_email

from utils import verify_password


def authenticate_user(email: str, password: str, db: Session):
    """Authenticate a user, check if their password is correct"""
    user = get_user_by_email(user_email=email, db=db)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user
