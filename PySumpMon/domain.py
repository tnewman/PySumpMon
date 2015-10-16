from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SumpWaterDistance(Base):
    __tablename__ = 'sump_pump_water_distances'

    id = Column(Integer, primary_key=True)
    water_distance_cm = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow())


class NotificationLog(Base):
    __tablename__ = 'notification_logs'

    id = Column(Integer, primary_key=True)
    to = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow())


class EventSuppression(Base):
    __tablename__ = 'event_suppressions'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    suppress_until = Column(DateTime, default=datetime.utcnow())
