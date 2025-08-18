from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ------------------ DB CONFIG ------------------

def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='0108',
        database='train2'
    )

# ------------------ SERIALIZER ------------------

def serialize_result(rows):
    for row in rows:
        for key in row:
            if isinstance(row[key], (bytes, bytearray)):
                row[key] = row[key].decode()
    return rows

# ------------------ ROUTES ------------------

# 🚨 CASES BY MONTH
@app.route('/cases/month', methods=['GET'])
def cases_by_month():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            SI_No,
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            Train_Name,
            TIME_FORMAT(Time, '%h:%i %p') AS Time,
            Case_ID,
            Report_Remark AS Remarks,
            CASE 
                WHEN Status = 1 THEN 'Closed'
                WHEN Status = 0 THEN 'Open'
                ELSE 'Unknown'
            END AS Case_Status,
            MONTH(Date) AS Month
        FROM final_report
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

# 🚨 CASES BY WEEK
@app.route('/cases/week', methods=['GET'])
def cases_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            SI_No,
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            Train_Name,
            TIME_FORMAT(Time, '%h:%i %p') AS Time,
            Case_ID,
            Report_Remark AS Remarks,
            CASE 
                WHEN Status = 1 THEN 'Closed'
                WHEN Status = 0 THEN 'Open'
                ELSE 'Unknown'
            END AS Case_Status,
            WEEK(Date, 1) AS Week
        FROM final_report
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

# 🚨 CASES BY YEAR
@app.route('/cases/year', methods=['GET'])
def cases_by_year():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            SI_No,
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            Train_Name,
            TIME_FORMAT(Time, '%h:%i %p') AS Time,
            Case_ID,
            Report_Remark AS Remarks,
            CASE 
                WHEN Status = 1 THEN 'Closed'
                WHEN Status = 0 THEN 'Open'
                ELSE 'Unknown'
            END AS Case_Status,
            YEAR(Date) AS Year
        FROM final_report
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

# 🚨 DAILY REPORT SUMMARY (Processed vs Pending)
@app.route('/report-summary/daily', methods=['GET'])
def report_summary_daily():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            DATE_FORMAT(Date, '%Y-%m-%d') AS Date,
            SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Processed,
            SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Pending
        FROM final_report
        GROUP BY Date
        ORDER BY Date;
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": serialize_result(rows)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

# ------------------ MAIN ------------------

if __name__ == '__main__':
    app.run(debug=True)