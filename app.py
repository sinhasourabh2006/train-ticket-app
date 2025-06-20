from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL config - replace with your actual credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9852',
    'database': 'train_ticket'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-ticket', methods=['POST'])
def save_ticket():
    data = request.get_json()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (pnr, from_station, to_station, passengers, datetime) VALUES (%s, %s, %s, %s, %s)",
               (data['pnr'], data['from'], data['to'], data['passengers'], data['datetime']))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Ticket saved to MySQL!'})

if __name__ == '__main__':
    app.run(debug=True)
