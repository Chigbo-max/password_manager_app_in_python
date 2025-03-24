import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers.emailserviceinterface import EmailServiceInterface


class GmailService(EmailServiceInterface):

    def __init__(self):
        self.smtp_server="smtp.gmail.com"
        self.smtp_port=587
        self.sender_email = os.getenv('GMAIL_SENDER_EMAIL')
        self.password = os.getenv('GMAIL_APP_PASSWORD')



    def send_email(self, to_email:str, subject:str, message:str):
        try:
            msg=MIMEMultipart()
            msg['From']=self.sender_email
            msg['To']=to_email
            msg['Subject']=subject

            msg.attach(MIMEText(message,'html'))

            server =  smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_email, msg.as_string())
            server.quit()

            return f"Kindly check for the password-reset-link sent to {to_email}"
        except Exception as e:
            return f"Email sending failed: {e}"


        except Exception as e:
            print(f"Email sending failed: {e}")

