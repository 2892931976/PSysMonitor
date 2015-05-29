import smtplib
import logger
import setting
from email.mime.text import MIMEText

def send_mail(receiver, title, message):
    logger.log("INFO", "[Mail Sender][To:%s][Title:%s][Message:%s]"%(receiver, title, message))
    mail_config = setting.mail_config()
    me = mail_config['smtp_sender']
    msg = MIMEText(message, _subtype="plain")
    msg["Subject"] = title
    msg["From"] = me
    msg["To"] = receiver
    try:
        server = smtplib.SMTP_SSL(mail_config['smtp_server'],mail_config['smtp_port'])
        server.login(mail_config['smtp_user'],mail_config['smtp_password'])
        server.sendmail(me, receiver, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

