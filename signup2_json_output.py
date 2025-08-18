from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import re

app = Flask(__name__)  # ✅ Fixed ___name___ (not __name__)
CORS(app)

# ------------------- DB CONFIG -------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sumuchamp@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- PASSWORD UTIL -------------------

def hash_password_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

# ------------------- VALIDATION -------------------

def is_valid_phone(phone):
    return str(phone).isdigit() and len(str(phone)) == 10

def is_valid_password(password):
    return len(password) >= 6  # Simple validation (change to 8+ if needed)

# ------------------- MODELS -------------------

class Station(db.Model):
    _tablename_ = 'station'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Station__name__ = db.Column(db.String(100))
    Station_Code = db.Column(db.String(20), unique=True)

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Station__name__': self.Station__name__,
            'Station_Code': self.Station_Code
        }

class Signup(db.Model):
    _tablename_ = 'signup'
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
            # ⚠ Don't include password in public responses
            'Name': self.Name
        }

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Train API!"})

@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

@app.route('/signup', methods=['GET'])
def show_signups():
    users = Signup.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/signup', methods=['POST'])
def create_signup():
    data = request.get_json()

    phone = data.get('Ph_No')
    password = data.get('Password')
    name = data.get('Name')
    station_code = data.get('Station_Code')
    user_type = data.get('Type_of_User')

    # ✅ Validations
    if not is_valid_phone(phone):
        return jsonify({'error': 'Phone number must be a 10-digit number.'}), 400

    if not is_valid_password(password):
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400

    if Signup.query.filter_by(Ph_No=phone).first():
        return jsonify({'error': 'Phone number already registered.'}), 409

    # ✅ Hash password before storing
    hashed_password = hash_password_sha1(password)

    new_user = Signup(
        Ph_No=phone,
        Station_Code=station_code,
        Type_of_User=user_type,
        Password=hashed_password,
        Name=name
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Signup successful!', 'user': new_user.to_dict()}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get("Ph_No")
    password = data.get("Password")

    user = Signup.query.filter_by(Ph_No=phone).first()

    if user:
        hashed_input = hash_password_sha1(password.strip())
        if user.Password == hashed_input:
            return jsonify({
                "status": "success",
                "message": f"Welcome {user.Name}!",
                "user": user.to_dict()
            })
    
    return jsonify({
        "status": "error",
        "message": "Invalid phone number or password"
    }), 401

# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)