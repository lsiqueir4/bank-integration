from models import BaseModel
from sqlalchemy import Column, CHAR, String


class Account(BaseModel):
    __tablename__ = "Account"

    account_key = Column(CHAR(36), nullable=False)
    bank_code = Column(String(8), nullable=False)
    branch_code = Column(String(10), nullable=False)
    account_number = Column(String(40), nullable=False)
