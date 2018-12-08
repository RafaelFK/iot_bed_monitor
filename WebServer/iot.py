from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="rkatopodis",
    password="Rlrf3606",
    hostname="rkatopodis.mysql.pythonanywhere-services.com",
    databasename="rkatopodis$bed_monitor",
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
    value = db.Column(db.Integer)

# Rotas e handlers
@app.route('/report', methods=['POST'])
def report():
    # Registrando leitura no banco
    sr = SensorReading(time=datetime.now(), value=request.json['value'])
    db.session.add(sr)
    db.session.commit()

    return "Received!"
