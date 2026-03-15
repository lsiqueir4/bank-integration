from models import BaseModel
from sqlalchemy import Column, String


class TransferStatus(BaseModel):
    __tablename__ = "TransferStatus"

    enumerator = Column(String(100), unique=True, nullable=False)
