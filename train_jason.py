from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime, date, time, timedelta

app = Flask(__name__)
CORS(app)

# ------------------- DATABASE CONFIG -------------------

def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='sumuchamp',   # ← Change if needed
        database='train2'
    )

# ------------------- SERIALIZER -------------------

def serialize_result(rows):
    for row in rows:
        for key in row:
            if isinstance(row[key], (datetime, date, time, timedelta)):
                row[key] = str(row[key])
    return rows

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return jsonify({"message": "✅ Train Report API is working!"})


# 🚆 1. Weekly Train Report
@app.route('/train-report/week', methods=['GET'])
def train_report_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                WEEK(Date, 1) AS Week, 
                Date, 
                Time, 
                Train_Name, 
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report
            ORDER BY Week;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()


# 🚆 2. Monthly Train Report
@app.route('/train-report/month', methods=['GET'])
def train_report_by_month():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                MONTH(Date) AS Month, 
                Date, 
                Time, 
                Train_Name, 
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report
            ORDER BY Month;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()


# 🚆 3. Yearly Train Report
@app.route('/train-report/year', methods=['GET'])
def train_report_by_year():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                YEAR(Date) AS Year, 
                Date, 
                Time, 
                Train_Name, 
                CASE WHEN Status = 1 THEN 'Finished' ELSE 'Pending' END AS Train_Status,
                Report_Remark AS Remarks
            FROM report
            ORDER BY Year;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

# ------------------- MAIN -------------------

if __name__ == '__main__':
    app.run(debug=True)
