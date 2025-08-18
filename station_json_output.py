from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB credentials for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sumuchamp@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- STATION MODEL ONLY -------------------

class Station(db.Model):
    __tablename__ = 'station'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Station_Name = db.Column(db.String(100))
    Station_Code = db.Column(db.String(20), unique=True)

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Station_Name': self.Station_Name,
            'Station_Code': self.Station_Code
        }

# ------------------- ROUTE -------------------

@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    station_list = [station.to_dict() for station in stations]
    return jsonify(station_list)

# ------------------- RUN APP -------------------

if __name__ == '__main__':
    with app.app_context():
        Station.__table__.create(db.engine, checkfirst=True)
    app.run(debug=True)
