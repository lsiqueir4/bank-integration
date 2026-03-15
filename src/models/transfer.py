from models import BaseModel
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class Transfer(BaseModel):
    __tablename__ = "Transfer"

    id = Column(Integer, primary_key=True)
    transfer_key = Column(String(36), nullable=False)
    external_id = Column(Integer, nullable=False, unique=True)
    account_id = Column(
        Integer, ForeignKey("stark_integration.Account.id"), nullable=False
    )
    amount = Column(Numeric(10, 2), nullable=False)
    transfer_status_id = Column(
        Integer, ForeignKey("stark_integration.TransferStatus.id"), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    account = relationship("Account")
    status = relationship("TransferStatus")
