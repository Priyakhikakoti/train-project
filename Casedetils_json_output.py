from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:0108@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- MODELS -------------------

class Station(db.Model):
    __tablename__ = 'station'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Station_Name = db.Column(db.String(100))
    Station_Code = db.Column(db.String(20), unique=True)

class Report(db.Model):
    __tablename__ = 'report'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_No = db.Column(db.String(20))
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

class UserDetails(db.Model):
    __tablename__ = 'userdetails'
    Ph_No = db.Column(db.BigInteger, primary_key=True)
    Name = db.Column(db.String(100))
    Age = db.Column(db.Integer)
    Email = db.Column(db.String(100))

class CaseDetails(db.Model):
    __tablename__ = 'casedetails'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'))
    Case_ID = db.Column(db.Integer)
    Case_Remark = db.Column(db.Text)
    Close = db.Column(db.Boolean)

# ------------------- ROUTES -------------------

@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    result = [
        {
            "SI_No": station.SI_No,
            "Station_Name": station.Station_Name,
            "Station_Code": station.Station_Code
        }
        for station in stations
    ]
    return jsonify(result)

@app.route('/reports')
def show_reports():
    reports = Report.query.all()
    result = [
        {
            "SI_No": report.SI_No,
            "Train_No": report.Train_No,
            "Report_ID": report.Report_ID,
            "Wagon_No": report.Wagon_No,
            "Coach_Position": report.Coach_Position,
            "Door_No": report.Door_No,
            "Camera_No": report.Camera_No,
            "Date": report.Date.isoformat() if report.Date else None,
            "Time": report.Time.isoformat() if report.Time else None,
            "Status": "Closed" if report.Status else "Open",
            "Report_Remark": report.Report_Remark,
            "Station_Code": report.Station_Code,
            "Case_ID": report.Case_ID,
            "Image_Link": report.Image_Link
        }
        for report in reports
    ]
    return jsonify(result)

@app.route('/users')
def show_users():
    users = UserDetails.query.all()
    result = [
        {
            "Ph_No": user.Ph_No,
            "Name": user.Name,
            "Age": user.Age,
            "Email": user.Email
        }
        for user in users
    ]
    return jsonify(result)

@app.route('/casedetails')
def show_case_details():
    cases = CaseDetails.query.all()
    result = [
        {
            "SI_No": case.SI_No,
            "Station_Code": case.Station_Code,
            "Case_ID": case.Case_ID,
            "Case_Remark": case.Case_Remark,
            "Status": "Closed" if case.Close else "Open"
        }
        for case in cases
    ]
    return jsonify(result)

# ------------------- RUN APP -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
