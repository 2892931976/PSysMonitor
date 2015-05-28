import smtplib
from email.mime.text import MIMEText

def send_mail(receiver, title, message):
    me = "psysmonitor<psysmonitor@sina.com>"
    msg = MIMEText(message, _subtype="plain")
    msg["Subject"] = title
    msg["From"] = me
    msg["To"] = receiver
    try:
        server = smtplib.SMTP_SSL("smtp.sina.com",465)
        server.login('psysmonitor','111222333')
        server.sendmail(me, receiver, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

