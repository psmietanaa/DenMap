import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.gmail.com"  # Set the server
mail_user = "XXX"  # User name
mail_pass = "XXX"  # Password

sender = 'XXX'  # The sender, which should be the same as mail_user
receivers = ['XXX']  # The receivers email


# Three parameters: first, the content of email; second, the subject of email
def send_mail(content, subject):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("DenMap Alert", 'utf-8')  # The name of sender
    message['To'] = Header("", 'utf-8')  # The name of receiver
    message['Subject'] = Header(subject, 'utf-8')  # Set the title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # Make connection to gmail. 465 is the port for gmail
        smtpObj.ehlo()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.close()
    except smtplib.SMTPException:
        print("Error while sending email")
