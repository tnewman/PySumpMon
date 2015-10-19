from datetime import datetime, timedelta
from flask import Flask, g, render_template
from PySumpMon import config, services
from serial import SerialException, SerialTimeoutException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from threading import Timer
from twilio.exceptions import TwilioException

app = Flask('pysumpmon')
app.db_engine = create_engine(config.DB_CONNECTION_STRING)
app.db_session_factory = sessionmaker(bind=app.db_engine)

distance_sensor = services.DistanceSensorService(
            config.DISTANCE_SENSOR_PORT)


def log_distance():
    next_log_time = datetime.utcnow() + timedelta(seconds=30)

    try:
        db_session = app.db_session_factory()

        event_suppression = services.EventSuppressionService(db_session)
        notification_log = services.NotificationLogService(db_session)
        sump_water_distance = services.SumpWaterDistanceService(db_session)

        twillio_sms = services.TwilioSMSService(
            config.TWILLIO_ACCOUNT, config.TWILLIO_TOKEN,
            config.TWILLIO_NOTIFICATION_FROM, config.TWILLIO_NOTIFICATION_TO)

        distance = distance_sensor.get_distance_cm()

        if distance:
            print('Distance: ' + str(distance) + ' cm')
            sump_water_distance.log_distance(distance)

            if distance < 10:
                if not event_suppression.get_suppressed_until():
                    try:
                        twillio_sms.send_sump_pump_level_high_message()
                        notification_log.log_notification(
                            config.TWILLIO_NOTIFICATION_TO)

                        current_time = datetime.utcnow()
                        suppress_delta = timedelta(minutes=30)
                        suppress_until = current_time + suppress_delta

                        event_suppression.suppress_event_until(suppress_until)

                        db_session.commit()
                    except TwilioException:
                        db_session.rollback()
        else:
            print('Could Not Log Distance - Invalid Sensor Value')
    except (SerialException, SerialTimeoutException):
        print('Could Not Log Distance - Serial Error')
        db_session.rollback()
    finally:
        db_session.close()

    timer_period = next_log_time - datetime.utcnow()

    log_distance_timer = Timer(timer_period.seconds, log_distance)
    log_distance_timer.start()

log_distance()


@app.before_request
def create_services():
    g.db_session = app.db_session_factory()
    g.event_suppression = services.EventSuppressionService(g.db_session)
    g.sump_water_distance = services.SumpWaterDistanceService(g.db_session)


@app.teardown_request
def close_db_session(errors):
    if errors is not None:
        g.db_session.rollback()

    g.db_session.close()


@app.route('/', methods=['GET'])
def show_sump_pump_water_distance():
    distance_logs = g.sump_water_distance.get_all_distance_logs()
    event_suppression = g.event_suppression.get_suppressed_until()

    return render_template('sumpwaterdistance.html',
                           distance_logs=distance_logs,
                           event_suppression=event_suppression)
