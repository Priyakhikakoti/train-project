from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your actual DB credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:0108@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- MODELS -------------------

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

class Report(db.Model):
    __tablename__ = 'report'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_Name = db.Column(db.String(50))
    Report_ID = db.Column(db.String(20), unique=True)
    Wagon_No = db.Column(db.Integer)
    Coach_Position = db.Column(db.Integer)
    Door_No = db.Column(db.Integer)
    Camera_No = db.Column(db.Integer)
    Date = db.Column(db.Date)
    Time = db.Column(db.Time)
    Status = db.Column(db.Boolean)
    Report_Remark = db.Column(db.Text)
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'))
    Case_ID = db.Column(db.Integer, unique=True)
    Image_Link = db.Column(db.String(255))
    Ph_No = db.Column(db.BigInteger)  # ✅ Added this line

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Train_Name': self.Train_Name,
            'Report_ID': self.Report_ID,
            'Wagon_No': self.Wagon_No,
            'Coach_Position': self.Coach_Position,
            'Door_No': self.Door_No,
            'Camera_No': self.Camera_No,
            'Date': self.Date.isoformat() if self.Date else None,
            'Time': self.Time.isoformat() if self.Time else None,
            'Status': 'Closed' if self.Status else 'Open',
            'Report_Remark': self.Report_Remark,
            'Station_Code': self.Station_Code,
            'Case_ID': self.Case_ID,
            'Image_Link': self.Image_Link,
            'Ph_No': self.Ph_No  # ✅ Added this line
        }

# ------------------- ROUTES -------------------

@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    station_list = [station.to_dict() for station in stations]
    return jsonify(station_list if station_list else {'message': 'No stations found'})

@app.route('/reports')
def show_reports():
    reports = Report.query.all()
    report_list = [report.to_dict() for report in reports]
    return jsonify(report_list if report_list else {'message': 'No reports found'})

# ------------------- RUN APP -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
