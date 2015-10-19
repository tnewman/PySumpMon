import re
import serial
import twilio.rest
from PySumpMon.domain import *
from sqlalchemy import desc


class DistanceSensorService:
    def __init__(self, com_port='COM1'):
        self.serial_port = None
        self.serial_port = serial.Serial(com_port, 115200)

    def open(self):
        self.serial_port.open()

    def get_distance_cm(self):
        try:
            serial_data = str(self.serial_port.readline(), 'ascii')

            while self.serial_port.inWaiting() > 0:
                serial_data = str(self.serial_port.readline(), 'ascii')

            # Regex Matches [Distance: XXX.XX]
            match = re.search('\[Distance:(\d+\.\d+)\]', serial_data)

            if match:
                distance = float(match.group(1))
                return distance
            else:
                return self.get_distance_cm()
        except serial.SerialException:
            return None

    def close(self):
        if self.serial_port:
            self.serial_port.close()

    def __del__(self):
        self.close()


class EventSuppressionService:
    def __init__(self, session):
        self.session = session

    def get_suppressed_until(self):
        suppress_until = self.session.query(EventSuppression).filter(
            EventSuppression.suppress_until > datetime.now()).order_by(
            desc(EventSuppression.suppress_until)).first()

        return suppress_until

    def suppress_event_until(self, suppress_until):
        event_suppression = EventSuppression()
        event_suppression.suppress_until = suppress_until
        self.session.add(event_suppression)
        self.session.commit()


class NotificationLogService:
    def __init__(self, session):
        self.session = session

    def get_last_notifiction(self):
        last_notification = self.session.query(NotificationLog) \
            .order_by(desc(NotificationLog.id)).first()

        return last_notification

    def log_notification(self, to):
        notification = NotificationLog()
        notification.to = to
        self.session.add(notification)


class SumpWaterDistanceService:
    def __init__(self, session):
        self.session = session

    def get_all_distance_logs(self):
        distance_logs = self.session.query(SumpWaterDistance).order_by(
            desc(SumpWaterDistance.id)).all()

        return distance_logs

    def log_distance(self, distance_cm):
        distance = SumpWaterDistance()
        distance.water_distance_cm = distance_cm
        self.session.add(distance)
        self.session.commit()


class TwilioSMSService:
    def __init__(self, account, token, from_number, to_number):
        self.twilio = twilio.rest.TwilioRestClient(account, token)
        self.from_number = from_number
        self.to_number = to_number

    def send_sump_pump_level_high_message(self):
        self.twilio.messages.create(to=self.to_number, from_=self.from_number,
                                    body='PySumpMon Warning: ' +
                                         'High sump pump level.')
