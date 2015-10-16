import re
import serial
import twilio.rest
from PySumpMon.domain import *
from sqlalchemy import desc


class DistanceSensorService:
    def __init__(self, com_port='COM1'):
        self.serial_port = serial.Serial(com_port, 115200)

    def open(self):
        self.serial_port.open()

    def get_distance_cm(self):
        try:
            serial_data = str(self.serial_port.readline(), 'ascii')

            # Regex Matches [Distance: XXX.XX]
            match = re.search('\[Distance:(\d+\.\d+)\]', serial_data)

            if match:
                return match.group(1)
            else:
                return None
        except serial.SerialException:
            return None

    def close(self):
        self.serial_port.close()

    def __del__(self):
        self.close()


class EventSuppressionService:
    def __init__(self, session):
        self.session = session

    def get_suppressed_until(self):
        suppress_until = self.session.query(EventSuppression).order_by(
            desc(EventSuppression.suppress_until)).limit(1).all()

        return suppress_until

    def suppress_event_until(self, suppress_until):
        event_suppression = EventSuppression()
        event_suppression.suppress_until = suppress_until
        self.session.add(event_suppression)


class SumpWaterDistanceService:
    def __init__(self, session):
        self.session = session

    def get_all_distance_logs(self):
        distance_logs = self.session.query(SumpWaterDistance).order_by(
            desc(SumpWaterDistance.timestamp)).all()

        return distance_logs

    def log_distance(self, distance_cm):
        distance = SumpWaterDistance()
        distance.water_distance_cm = distance_cm
        self.session.add(distance)


class NotificationLogService:
    def __init__(self, session):
        self.session = session

    def get_last_notifiction(self):
        last_notification = self.session.query(NotificationLog) \
            .order_by(NotificationLog.id.desc()).first()

        return last_notification

    def log_notification(self, to, message):
        notification = NotificationLog()
        notification.to = to
        notification.message = message
        self.session.add(notification)


class TwilioSMSService:
    def __init__(self, account, token, from_number, to_number):
        self.twilio = twilio.rest.TwilioRestClient(account, token)
        self.from_number = from_number
        self.to_number = to_number

    def send_sump_pump_level_high_message(self):
        self.twilio.messages.create(to=self.to_number, from_=self.from_number,
                                    body='PySumpMon Warning: ' +
                                         'High sump pump level.')
