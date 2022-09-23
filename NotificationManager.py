import os, smtplib
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

class NotificationManager:
    def send_text(messages):
        account_sid = os.getenv('ACC_SID')
        auth_token = os.getenv('ACC_TOKEN')
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=messages,
                            from_=os.getenv('PHONE_NUMBER'),
                            to=os.getenv('MY_NUMBER')
                        )
    
    def send_email(message):
        conn = smtplib.SMTP('smtp.gmail.com', 587)
        conn.ehlo()
        conn.starttls()
        conn.login(os.getenv('FROM_EMAIL'), os.getenv('FROM_EMAIL_PASSWORD'))
        conn.sendmail(os.getenv('FROM_EMAIL'), os.getenv('EMAIL'), message)
        conn.quit()