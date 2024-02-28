import os
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv

# Getting all environment variables and loading them to memory
load_dotenv()


class Secret:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PER_UNIT_COST_IN_RUPEES: float
    PER_UNIT_PEAK_FACTOR_COST_IN_RUPEES: float

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: float | str,
        per_unit_cost_in_rupees,
        per_unit_peak_factor_cost_in_rupess,
    ) -> None:
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_minutes)
        self.PER_UNIT_COST_IN_RUPEES = float(per_unit_cost_in_rupees)
        self.PER_UNIT_PEAK_FACTOR_COST_IN_RUPEES = float(
            per_unit_peak_factor_cost_in_rupess
        )


secret = Secret(
    secret_key=os.getenv("SECRET_KEY"),
    algorithm=os.getenv("ALGORITHM"),
    access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
    per_unit_cost_in_rupees=os.getenv("PER_UNIT_COST_IN_RUPEES"),
    per_unit_peak_factor_cost_in_rupess=os.getenv(
        "PER_UNIT_PEAK_FACTOR_COST_IN_RUPEES"
    ),
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def are_object_to_edit_and_other_object_same_by_nic(
    obj_to_edit, other_object_with_same_nic
) -> bool:
    """Check if the object you are editing is the same as unique constraint conflict other_object"""
    return (
        True
        if obj_to_edit.nic_number == other_object_with_same_nic.nic_number
        else False
    )


def are_object_to_edit_and_other_object_same_by_email(
    obj_to_edit, other_object_with_same_email
) -> bool:
    """Check if the object you are editing is the same as unique constraint conflict other_object"""
    return True if obj_to_edit.email == other_object_with_same_email.email else False


def return_datetime_in_proper_format() -> datetime:
    """Returns the datetime object, in proper format which is same as database"""
    current_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    return datetime.strptime(current_timestamp, "%Y-%m-%dT%H:%M:%S")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the provided plain and hashed password strings match"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> bool:
    """Generate a hash for the provided password string"""
    return pwd_context.hash(password)


def create_access_token(
    data: dict, expires_delta: timedelta, key: str, algorithm: str
) -> str:
    """Generate JWT based access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=key, algorithm=algorithm)
    return encoded_jwt


def return_per_unit_cost_depending_on_time() -> float:
    current_time = datetime.now()
    datetime_6pm = datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day,
        hour=18,
        minute=0,
    )
    datetime_10pm = datetime_6pm + timedelta(hours=4)

    if current_time >= datetime_6pm and current_time <= datetime_10pm:
        return float(secret.PER_UNIT_PEAK_FACTOR_COST_IN_RUPEES)
    else:
        return float(secret.PER_UNIT_COST_IN_RUPEES)
