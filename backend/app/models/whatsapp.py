from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.database import Base

class WhatsappMessage(Base):
    __tablename__ = "whatsapp_messages"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(50), index=True)
    sender_name = Column(String(100), nullable=True)
    message_body = Column(Text, nullable=False)
    response_body = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
