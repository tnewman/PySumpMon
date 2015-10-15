from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, DECIMAL


class SumpWaterDistance:
    __tablename__ = 'sump_pump_water_distances'

    id = Column(Integer, primary_key=True)
    water_distance = Column(DECIMAL)
    timestamp = Column(DateTime, default=datetime.utcnow())


class NotificationLog:
    __tablename__ = 'notification_log'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())


class EventSuppression:
    __tablename__ = 'event_suppression'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
