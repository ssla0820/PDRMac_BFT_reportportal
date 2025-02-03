# import smtplib
# import os

# from email.mime.text import MIMEText

# gmail_user = 'clsignupstress@gmail.com'
# with open(os.path.dirname(__file__)+"//p.txt", "r") as f:
    # gmail_password = f.read()

 
# msg = MIMEText('content')
# msg['Subject'] = 'Test'
# msg['From'] = gmail_user
# msg['To'] = gmail_user

# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.ehlo()
# server.login(gmail_user, gmail_password)
# server.send_message(msg)
# server.quit()

# print('Email sent!')

''''''
import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

def send_mail(opts):
    # set info
    fileRead = lambda fileName,mode="r": open(os.path.dirname(__file__)+"//"+filename,mode)
    me = opts['account']
    you = opts['to']
    password = opts['password']

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = opts['subject']
    msg['From'] = opts['from']
    #msg['To'] = ",".join(you)
    msg['To'] = str(you)

    # Message data info
    text = opts['text']
    html = opts['html']
    attachment = opts['attachment']

    # Transfer data
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html','utf-8')
    # att = MIMEText(attachment, 'base64', 'utf-8')
    # att["Content-Type"] = 'application/octet-stream'
    # att["Content-Disposition"] = 'attachment; filename="BFT_Report.html"'

    # Attach data into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    #msg.attach(att)
    for f in opts['attachment']:
        with open("{}\\{}".format(os.path.dirname(os.path.abspath(__file__)), f), "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(me, password)
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
    
if __name__ == '__main__':
    opts = {
        "account":"cyberlinkqamc@gmail.com"
        ,"password":"qamc1234"
        ,"from":"QAServer <cyberlinkqamc@gmail.com>"
        ,"to": ["jim_huang@cyberlink.com"]
        ,"subject": "[AT] Auto TR Build Download Module Error"
        ,"text": "text_content"
        ,"html": "this is the sample error"
        ,"attachment": []
    }
    send_mail(opts)