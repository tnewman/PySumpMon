import datetime
from flask import Flask, g, render_template, redirect, url_for
from PySumpMon import config, services
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask('pysumpmon')
app.db_engine = create_engine(config.DB_CONNECTION_STRING)
app.db_session_factory = sessionmaker(bind=app.db_engine)


@app.before_request
def create_services():
    g.db_session = app.db_session_factory()
    g.EventSuppressionService = services.EventSuppressionService(g.db_session)
    g.NotificationLogService = services.NotificationLogService(g.db_session)
    g.SumpWaterDistanceService = services.SumpWaterDistanceService(
        g.db_session)


@app.teardown_request
def close_db_session(errors):
    if errors is not None:
        g.db_session.rollback()

    g.db_session.close()


@app.route('/', methods=['GET'])
def show_sump_pump_water_distance():
    distance_logs = g.SumpWaterDistanceService.get_all_distance_logs()

    event_suppression = g.EventSuppressionService.get_suppressed_until()

    return render_template('sumpwaterdistance.html',
                           distance_logs=distance_logs,
                           event_suppression=event_suppression)
