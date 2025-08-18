from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔧 MySQL Connection Function
def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='0108',  # Update if needed
        database='train2'
    )

# 📊 Monthly Summary
@app.route('/report-summary/monthly', methods=['GET'])
def monthly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                YEAR(Date) AS Year,
                MONTH(Date) AS Month,
                COUNT(*) AS Finished_Reports
            FROM final_report
            WHERE Status = 1
            GROUP BY YEAR(Date), MONTH(Date)
            ORDER BY Year, Month;
        """)
        data = cursor.fetchall()
        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# 📊 Weekly Summary
@app.route('/report-summary/weekly', methods=['GET'])
def weekly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                YEAR(Date) AS Year,
                WEEK(Date) AS Week,
                COUNT(*) AS Finished_Reports
            FROM final_report
            WHERE Status = 1
            GROUP BY YEAR(Date), WEEK(Date)
            ORDER BY Year, Week;
        """)
        data = cursor.fetchall()
        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# 📊 Yearly Summary
@app.route('/report-summary/yearly', methods=['GET'])
def yearly_summary():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                YEAR(Date) AS Year,
                COUNT(*) AS Finished_Reports
            FROM final_report
            WHERE Status = 1
            GROUP BY YEAR(Date)
            ORDER BY Year;
        """)
        data = cursor.fetchall()
        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# 🏁 Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
