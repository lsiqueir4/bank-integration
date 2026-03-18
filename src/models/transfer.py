from models import BaseModel
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship


class Transfer(BaseModel):
    __tablename__ = "Transfer"

    transfer_key = Column(String(36), nullable=False)
    external_id = Column(String(255), unique=True)
    account_id = Column(
        Integer, ForeignKey("stark_integration.Account.id"), nullable=False
    )
    amount = Column(Numeric(10, 2), nullable=False)
    transfer_status_id = Column(
        Integer, ForeignKey("stark_integration.TransferStatus.id"), nullable=False
    )

    account = relationship("Account")
    status = relationship("TransferStatus")
