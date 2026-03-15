from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {"schema": "stark_integration"}
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
