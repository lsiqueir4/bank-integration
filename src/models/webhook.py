from sqlalchemy import Column, Integer, String, CHAR, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from models import BaseModel


class Webhook(BaseModel):
    __tablename__ = "Webhook"

    webhook_key = Column(CHAR(36), nullable=False)
    external_id = Column(String(255), unique=True)
    webhook_type_id = Column(Integer, ForeignKey("stark_integration.WebhookType.id"))
    webhook_status_id = Column(
        Integer, ForeignKey("stark_integration.WebhookStatus.id"), nullable=False
    )
    payload = Column(JSONB, nullable=False)
    failure_reason = Column(String(255))

    webhook_type = relationship("WebhookType")
    status = relationship("WebhookStatus")
