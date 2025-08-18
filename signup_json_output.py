from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB credentials for MySQL (change accordingly if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sumuchamp@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- STATION MODEL -------------------

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

# ------------------- SIGNUP MODEL -------------------

class Signup(db.Model):
    __tablename__ = 'signup'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ph_No = db.Column(db.BigInteger, unique=True)
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'), nullable=True)
    Type_of_User = db.Column(db.String(50))
    Password = db.Column(db.String(100))
    Name = db.Column(db.String(100))

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Ph_No': self.Ph_No,
            'Station_Code': self.Station_Code,
            'Type_of_User': self.Type_of_User,
            'Password': self.Password,
            'Name': self.Name
        }

# ------------------- ROUTES -------------------

@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

@app.route('/signup')
def show_signups():
    users = Signup.query.all()
    return jsonify([user.to_dict() for user in users])

# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if not already created
    app.run(debug=True)
