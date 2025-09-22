from sqlalchemy import Column, Integer, String
from .database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    msg = Column(String, nullable=True)
