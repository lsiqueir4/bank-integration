from models import BaseModel
from sqlalchemy import Column, String


class InvoiceStatus(BaseModel):
    __tablename__ = "InvoiceStatus"

    enumerator = Column(String(100), unique=True, nullable=False)
