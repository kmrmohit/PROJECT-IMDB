import smtplib
import config

def send_email(subject,msg):
   
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAILADDRESS,config.PASSWORD)
        message = 'Subject:{}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAILADDRESS,config.EMAILADDRESS,message)
        server.close()
        print("SUCCESS")



subject="test subject"
msg = "hello"
send_email(subject,msg)
