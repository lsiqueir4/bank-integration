from models import BaseModel
from sqlalchemy import Column, CHAR, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Account(BaseModel):
    __tablename__ = "Account"

    account_key = Column(CHAR(36), nullable=False)
    bank_code = Column(String(8), nullable=False)
    branch_code = Column(String(10), nullable=False)
    account_number = Column(String(40), nullable=False)
    owner_document_number = Column(String(18), nullable=False)
    owner_name = Column(String(255), nullable=False)
    account_type_id = Column(
        Integer, ForeignKey("stark_integration.AccountType.id"), nullable=False
    )

    account_type = relationship("AccountType")
