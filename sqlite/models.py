from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlite.database import Base, engine
from sqlite.schemas import UserUpdateWithoutCustomer, CustomerCreateOrUpdate

Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    customer = relationship("Customer", uselist=False, cascade="all,delete")

    created_at = Column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    def update(self, user: UserUpdateWithoutCustomer, **kwargs):
        self.name = user.name
        self.email = user.email


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    nic_number = Column(String, index=True, nullable=False, unique=True)
    watts_consumed = Column(Float, nullable=False, default=0.0)
    account_balance_in_rupees = Column(Integer, nullable=False)
    should_get_service = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    def update(self, cux: CustomerCreateOrUpdate, **kwargs):
        self.nic_number = cux.nic_number
