from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
import hashlib

app = Flask(__name__)
CORS(app)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_super_secret_key_here'

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:0108@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- MODELS -------------------

class Station(db.Model):
    __tablename__ = 'station'
    SI_No = db.Column(db.Integer, primary_key=True)
    Station_Name = db.Column(db.String(100))
    Station_Code = db.Column(db.String(20), unique=True)

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Station_Name': self.Station_Name,
            'Station_Code': self.Station_Code
        }

class Signup(db.Model):
    __tablename__ = 'signup'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ph_No = db.Column(db.BigInteger, unique=True)
    Name = db.Column(db.String(100))
    Password = db.Column(db.String(100))  # SHA1 hash
    Type_of_User = db.Column(db.String(50))
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'))

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Ph_No': self.Ph_No,
            'Name': self.Name,
            'Type_of_User': self.Type_of_User,
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
    Ph_No = db.Column(db.BigInteger)

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
            'Status': "Closed" if self.Status else "Open",
            'Report_Remark': self.Report_Remark,
            'Station_Code': self.Station_Code,
            'Case_ID': self.Case_ID,
            'Image_Link': self.Image_Link,
            'Ph_No': self.Ph_No
        }



def hash_password_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Signup.query.get(data['user_id'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return jsonify({"message": "Hello from the Flask backend 🔥"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    phone = data['Ph_No']
    password = data['Password']
    name = data['Name']
    station_code = data['Station_Code']
    user_type = data['Type_of_User']

    if Signup.query.filter_by(Ph_No=phone).first():
        return jsonify({'error': 'Phone number already registered.'}), 409

    hashed_pw = hash_password_sha1(password)
    new_user = Signup(
        Ph_No=phone,
        Name=name,
        Password=hashed_pw,
        Station_Code=station_code,
        Type_of_User=user_type
    )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({
        'user_id': new_user.SI_No,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        'message': 'Signup successful!',
        'user': new_user.to_dict(),
        'token': token
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get("Ph_No")
    password = data.get("Password")
    user = Signup.query.filter_by(Ph_No=phone).first()

    if user and user.Password == hash_password_sha1(password):
        token = jwt.encode({
            'user_id': user.SI_No,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "message": f"Welcome {user.Name}!",
            "token": token,
            "user": user.to_dict()
        })

    return jsonify({"error": "Invalid phone number or password"}), 401

@app.route('/addreport', methods=['POST'])
@token_required
def add_report(current_user):
    data = request.get_json()

    try:
        report = Report(
            Train_Name=data['Train_Name'],
            Report_ID=data['Report_ID'],
            Wagon_No=data['Wagon_No'],
            Coach_Position=data['Coach_Position'],
            Door_No=data['Door_No'],
            Camera_No=data['Camera_No'],
            Date=datetime.datetime.strptime(data['Date'], '%Y-%m-%d').date(),
            Time=datetime.datetime.strptime(data['Time'], '%H:%M:%S').time(),
            Status=data['Status'],
            Report_Remark=data['Report_Remark'],
            Station_Code=data['Station_Code'],
            Case_ID=data['Case_ID'],
            Image_Link=data['Image_Link'],
            Ph_No=current_user.Ph_No
        )

        db.session.add(report)
        db.session.commit()
        return jsonify({'message': 'Report added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    return jsonify([report.to_dict() for report in reports])

@app.route('/update-report', methods=['POST'])
@token_required
def update_report(current_user):
    data = request.get_json()
    report_id = data.get('Report_ID')
    new_name = data.get('Train_Name')
    new_status = data.get('Status')

    if not report_id or new_name is None or new_status is None:
        return jsonify({'error': 'Missing required fields'}), 400

    report = Report.query.filter_by(Report_ID=report_id).first()

    if not report:
        return jsonify({'error': 'Report not found'}), 404

    try:
        report.Train_Name = new_name
        report.Status = new_status
        db.session.commit()

        return jsonify({
            'message': 'Report updated successfully!',
            'updated_report': report.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
