from flask import Flask, request, render_template
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# SQLite database initialization
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
''')
conn.commit()

# Email configuration (replace with your own email credentials)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'

def send_email(name, email, message):
    subject = 'New Message from Chatbot'
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Store data in the database
        cursor.execute('INSERT INTO users (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()

        # Send email notification
        send_email(name, email, message)

        return render_template('success.html', name=name)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
