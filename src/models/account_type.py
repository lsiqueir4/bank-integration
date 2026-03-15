from models import BaseModel
from sqlalchemy import Column, String


class AccountType(BaseModel):
    __tablename__ = "AccountType"

    enumerator = Column(String(100), unique=True, nullable=False)
