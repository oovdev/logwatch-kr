# app/services/alert_service.py

import smtplib
from email.mime.text import MIMEText
import smtplib
from email.mime.text import MIMEText
import os

def should_alert(log_level: str, message: str) -> bool:
    # 'ERROR' 레벨 로그일 경우에만 알림
    return log_level.upper() == "ERROR"

def send_email_alert(subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("ALERT_EMAIL_FROM")
    msg["To"] = os.getenv("ALERT_EMAIL_TO")

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        # TLS 사용 여부 확인 후 설정
        if os.getenv("SMTP_USE_TLS", "false").lower() == "true":
            server.starttls()
        
        username = os.getenv("SMTP_USERNAME")
        password = os.getenv("SMTP_PASSWORD")

        if username and password:
            server.login(username, password)

        server.send_message(msg)

def send_alert(hostname: str, message: str):
    from_addr = "logwatch@test.local"
    to_addr = "admin@test.local"
    subject = f"[ALERT] {hostname}"
    body = f"[ALERT from {hostname}] {message}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    try:
        with smtplib.SMTP("localhost", 1025) as server:
            server.send_message(msg)
        print("Email alert sent.")
    except Exception as e:
        print(f"Email sending failed: {e}")
