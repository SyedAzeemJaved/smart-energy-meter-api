from datetime import datetime
from pydantic import BaseModel, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str
    user: "User"


class TokenData(BaseModel):
    email: str | None = None


class CustomResponseBase(BaseModel):
    detail: str


class ErrorResponseBase(CustomResponseBase):
    pass


class Custom403ErrorResponse(ErrorResponseBase):
    pass


class Custom404ErrorResponse(ErrorResponseBase):
    pass


class CustomSuccessResponse(CustomResponseBase):
    pass


# Customer
class CustomerBase(BaseModel):
    nic_number: str

    @field_validator("nic_number")
    @classmethod
    def nic_validator(cls, v: str) -> str:
        if len(v) != 13:
            raise ValueError("must be 13 digits long")
        if " " in v:
            raise ValueError("must not contain a space")
        if "-" in v:
            raise ValueError("must not contain any dashes")
        return v


class CustomerCreateOrUpdate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    units_consumed: float
    account_balance_in_rupees: float
    should_get_service: bool

    previous_voltage_reading: float
    previous_current_reading: float

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class CustomerReadingBase(BaseModel):
    voltage: float
    current: float
    units_consumed: float

    @field_validator("voltage", "current")
    @classmethod
    def value_validator(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("must be a positive value")
        return v


class CustomerTopupAccountBalanceBase(BaseModel):
    account_balance_in_rupees: float

    @field_validator("account_balance_in_rupees")
    @classmethod
    def value_validator(cls, v: float) -> float:
        if v < 0:
            raise ValueError("must be greater than zero")
        return v


# User
class UserBase(BaseModel):
    name: str
    email: str

    @field_validator("email")
    @classmethod
    def email_validator(cls, v: str) -> str:
        if " " in v:
            raise ValueError("must not contain a space")
        if "," in v:
            raise ValueError("must not contain any commas")
        if not "@" in v:
            raise ValueError("must be a valid email address")
        return v


class UserCreateBase(UserBase):
    password: str


class UserAdminCreate(UserCreateBase):
    pass


class UserCustomerCreate(UserCreateBase):
    customer: CustomerCreateOrUpdate


class UserUpdateWithoutCustomer(UserBase):
    pass


class UserUpdateWithCustomer(UserBase):
    customer: CustomerCreateOrUpdate


class UserPasswordChange(UserBase):
    new_password: str


class UserOrmBase(UserBase):
    id: int
    is_admin: bool = False

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class UserAdmin(UserOrmBase):
    pass


class User(UserOrmBase):
    id: int
    is_admin: bool = False
    customer: Customer | None = None

    created_at: datetime
    updated_at: datetime | None


Token.model_rebuild()
