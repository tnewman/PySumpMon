from flask import Flask, g, render_template
from PySumpMon import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask('pysumpmon')
app.db_engine = create_engine(config.DB_CONNECTION_STRING)
app.db_session_factory = sessionmaker(bind=app.db_engine)


@app.before_request
def create_db_session2():
    g.db_session = app.db_session_factory()


@app.teardown_request
def close_db_session(errors):
    if errors is not None:
        g.db_session.rollback()

    g.db_session.close()


@app.route('/', methods=['GET'])
def show_sump_pump_water_distance():
    return render_template('sumpwaterdistance.html')
