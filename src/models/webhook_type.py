from models import BaseModel
from sqlalchemy import Column, String


class WebhookType(BaseModel):
    __tablename__ = "WebhookType"

    enumerator = Column(String(100), unique=True, nullable=False)
