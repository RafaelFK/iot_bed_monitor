from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import json

app = Flask(__name__)

# Configuração do banco de dados
with open('config.json') as config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username=config["db_user"],
        password=config["db_pass"],
        hostname=config["db_host"],
        databasename=config["db_name"],
    )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Model representando leituras de sensores
class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    value_11 = db.Column(db.Float)
    value_12 = db.Column(db.Float)
    value_21 = db.Column(db.Float)
    value_22 = db.Column(db.Float)
    value_31 = db.Column(db.Float)
    value_32 = db.Column(db.Float)

# Rotas e handlers
@app.route('/')
def index():
    return render_template('index.html', readings=SensorReading.query.order_by(db.desc(SensorReading.time)).limit(10).all())


@app.route('/latest')
def latest():
    # return db.session.query(SensorReading).order_by(db.desc(SensorReading.id)).first()
    reading = SensorReading.query.order_by(SensorReading.id.desc()).first()

    return jsonify({
        'timestamp': reading.time,
        'value_11': reading.value_11,
        'value_12': reading.value_12,
        'value_21': reading.value_21,
        'value_22': reading.value_22,
        'value_31': reading.value_31,
        'value_32': reading.value_32
    })

@app.route('/report', methods=['POST'])
def report():
    # Registrando leitura no banco
    sr = SensorReading(
        time=datetime.now(),
        value_11=request.json['value_11'],
        value_12=request.json['value_12'],
        value_21=request.json['value_21'],
        value_22=request.json['value_22'],
        value_31=request.json['value_31'],
        value_32=request.json['value_32']
    )

    db.session.add(sr)
    db.session.commit()

    return "Received!"