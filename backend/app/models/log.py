from sqlalchemy import Column, Float, Integer, String
from app.db.database import Base

class GestureLog(Base):
    __tablename__ = 'gesture_logs'
    id = Column(Integer, primary_key=True, index=True)
    predicted_label = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    action_triggered = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
