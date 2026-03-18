from models import BaseModel
from sqlalchemy import Column, String


class WebhookStatus(BaseModel):
    __tablename__ = "WebhookStatus"

    enumerator = Column(String(100), unique=True, nullable=False)
