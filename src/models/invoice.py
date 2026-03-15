from models import BaseModel
from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, Numeric
from sqlalchemy.orm import relationship


class Invoice(BaseModel):
    __tablename__ = "Invoice"

    invoice_key = Column(CHAR(36), nullable=False)
    payer_document_number = Column(String(14), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    fee_amount = Column(Numeric(10, 2))
    external_id = Column(Integer, unique=True, nullable=False)
    invoice_status_id = Column(
        Integer, ForeignKey("stark_integration.InvoiceStatus.id")
    )
    pdf_url = Column(String(255))
    barcode = Column(String(255))
    name = Column(String(255), nullable=False)

    status = relationship("InvoiceStatus")
