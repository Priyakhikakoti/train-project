from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔧 MySQL Connection Config
def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='0108',  # Change if different
        database='train2'
    )

# 1️⃣ Reports by Date
@app.route('/reports/by-date', methods=['GET'])
def reports_by_date():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT  
              Date,
              CASE 
                WHEN Status = 1 THEN 'Finished'
                ELSE 'Unfinished'
              END AS Report_Status,
              COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY Date, Status
            ORDER BY Date;
        """)
        return jsonify({"status": "success", "data": cursor.fetchall()})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        cursor.close()
        conn.close()

# 2️⃣ Reports by Month
@app.route('/reports/by-month', methods=['GET'])
def reports_by_month():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
              MONTH(Date) AS Month,
              CASE 
                WHEN Status = 1 THEN 'Finished'
                ELSE 'Unfinished'
              END AS Report_Status,
              COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY MONTH(Date), Status
            ORDER BY Month;
        """)
        return jsonify({"status": "success", "data": cursor.fetchall()})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        cursor.close()
        conn.close()

# 3️⃣ Reports by Week
@app.route('/reports/by-week', methods=['GET'])
def reports_by_week():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
              WEEK(Date, 1) AS Week,
              CASE 
                WHEN Status = 1 THEN 'Finished'
                ELSE 'Unfinished'
              END AS Report_Status,
              COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY WEEK(Date, 1), Status
            ORDER BY Week;
        """)
        return jsonify({"status": "success", "data": cursor.fetchall()})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        cursor.close()
        conn.close()

# 4️⃣ Reports by Year
@app.route('/reports/by-year', methods=['GET'])
def reports_by_year():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
              YEAR(Date) AS Year,
              CASE 
                WHEN Status = 1 THEN 'Finished'
                ELSE 'Unfinished'
              END AS Report_Status,
              COUNT(*) AS Total_Reports
            FROM final_report
            GROUP BY YEAR(Date), Status
            ORDER BY Year;
        """)
        return jsonify({"status": "success", "data": cursor.fetchall()})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        cursor.close()
        conn.close()

# 🚀 Run App
if __name__ == '__main__':
    app.run(debug=True)
