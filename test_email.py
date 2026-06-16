from email.message import EmailMessage
import smtplib

SMTP_HOST = "mail.datapowered.tech"
SMTP_PORT = 465
SMTP_USER = "agent@datapowered.tech"
SMTP_PASS = "ptjis9EUcFcnCpL"

msg = EmailMessage()
msg["From"] = SMTP_USER
msg["To"] = "mihai.rdu@gmail.com"
msg["Subject"] = "SMTP test from Bluehost"
msg.set_content("Test email from Python.")

with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
    server.set_debuglevel(1)
    server.login(SMTP_USER, SMTP_PASS)
    result = server.send_message(msg)
    print("Send result:", result)