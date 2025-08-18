from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your actual DB credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sumuchamp@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- MODEL -------------------

class FinalReport(db.Model):
    __tablename__ = 'final_report'

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
    Station_Code = db.Column(db.String(20))
    Station_Name = db.Column(db.String(100))
    Case_ID = db.Column(db.Integer, unique=True)
    Image_Link = db.Column(db.String(255))
    Ph_No = db.Column(db.BigInteger)
    User_Name = db.Column(db.String(100))
    User_Age = db.Column(db.Integer)
    User_Email = db.Column(db.String(100))

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
            'Station_Name': self.Station_Name,
            'Case_ID': self.Case_ID,
            'Image_Link': self.Image_Link,
            'Ph_No': self.Ph_No,
            'User_Name': self.User_Name,
            'User_Age': self.User_Age,
            'User_Email': self.User_Email
        }

# ------------------- ROUTE -------------------

@app.route('/final_report')
def show_final_report():
    reports = FinalReport.query.limit(10).all()
    report_list = [report.to_dict() for report in reports]
    return jsonify(report_list if report_list else {'message': 'No records found'})

# ------------------- RUN APP -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
