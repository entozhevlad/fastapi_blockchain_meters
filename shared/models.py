# shared/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, func
from .database import Base


class Blockchain(Base):
    __tablename__ = "blockchain"

    index = Column(Integer, primary_key=True, index=True)
    previous_hash = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class MeterData(Base):
    __tablename__ = "meter_data"

    meter_id = Column(String, primary_key=True)
    consumption = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), primary_key=True)
