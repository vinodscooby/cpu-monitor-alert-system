from flask import Flask, jsonify
import psutil
import time
import os
from threading import Thread
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)

ALERT_THRESHOLD = 30   # Change to 30 for testing

def send_alert(cpu, memory):
    try:
        msg = MIMEText(f"High Resource Usage Alert!\n\nCPU: {cpu}%\nMemory: {memory}%\nTime: {time.ctime()}")
        msg['Subject'] = f'⚠️ DevOps Alert - High CPU/Memory Usage'
        msg['From'] = os.getenv('EMAIL_ADDRESS')
        msg['To'] = os.getenv('EMAIL_ADDRESS')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
        print("✅ Alert Sent")
    except Exception as e:
        print(f"Alert failed: {e}")

def monitor_resources():
    while True:
        cpu = psutil.cpu_percent(interval=5)
        memory = psutil.virtual_memory().percent
        
        print(f"CPU: {cpu}% | Memory: {memory}%")
        
        if cpu > ALERT_THRESHOLD or memory > 80:
            send_alert(cpu, memory)
            time.sleep(300)  # 5 min cooldown
        time.sleep(10)

@app.route('/')
def dashboard():
    return f"""
    <h1>DevOps Monitoring Dashboard - Project 3</h1>
    <h2>CPU: {psutil.cpu_percent()}%</h2>
    <h2>Memory: {psutil.virtual_memory().percent}%</h2>
    <p><b>Alert Threshold:</b> {ALERT_THRESHOLD}% CPU</p>
    <p>GitHub Actions CI/CD + Real-time Monitoring</p>
    """

@app.route('/metrics')
def metrics():
    """For Prometheus / Monitoring tools"""
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "timestamp": time.time()
    })

if __name__ == '__main__':
    Thread(target=monitor_resources, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)