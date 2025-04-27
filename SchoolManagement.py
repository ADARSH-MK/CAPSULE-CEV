from flask import Flask, render_template, request, redirect, url_for, flash
import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import os

app = Flask(__name__)

# Secret key for flash messages
app.secret_key = 'abc123!@#secret'

# Google Sheets API Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1EqhWWY3bHzlM1WXDaGSulhZ70dPM7BdfzK_Wg7S2Cnc'
RANGE_NAME = 'Sheet1!A:B'  # Assuming usernames are in column A and passwords in column B

# Authenticate using Environment Variable
service_account_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Read data from Google Sheet
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            flash('No data found in sheet.', 'error')
            return redirect(url_for('home'))

        # Check username and password
        for row in values:
            if len(row) >= 2:
                sheet_username = row[0]
                sheet_password = row[1]
                if username == sheet_username and password == sheet_password:
                    return redirect(url_for('dashboard'))

        # If no match found
        flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
