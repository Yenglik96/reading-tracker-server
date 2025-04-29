from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Google Sheets-ке қосылу
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/readingtrackerbot-99658a293973.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Reading Tracker").sheet1  # <-- Sheets атауы

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    book = data.get('book')
    minutes = data.get('minutes')
    seconds = data.get('seconds')

    reading_time = f"{minutes} минут {seconds} секунд"
    today_date = datetime.now().strftime("%d.%m.%Y")

    sheet.append_row([name, book, reading_time, today_date])
    print(f"Аты: {name}, Кітап: {book}, Уақыты: {reading_time}, Күні: {today_date}")

    return jsonify({"message": "Дерек Google Sheets-ке сәтті жазылды!"})

@app.route('/')
def home():
    return "📚 Reading Tracker Server is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ← МІНДЕТТІ түрде 5000 болу керек!
    app.run(host='0.0.0.0', port=port, debug=True)
