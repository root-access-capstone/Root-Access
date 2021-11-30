# Third Party
import smtplib
import time
import socket


GMAILUSER = 'rootaccesplant@gmail.com'
GMAILPASSWORD = 'rootaccess2022'

EMAILLIST = ['leaderfirestar@ksu.edu', 'jrmartin@ksu.edu', 'aquariuswre@ksu.edu']

def notifyLowWater(currentTime):
    subject = 'ROOT ACCESS: Your plant needs water'
    date = time.localtime(currentTime)
    localDate = time.asctime(date)
    body = f'Attention Users! The water levels in your system are low as of {localDate}, and it needs to be refilled'
    emailText = '''\n
    From: %s
    To: %s
    Subject: %s

    %s
    '''%(GMAILUSER, EMAILLIST, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(GMAILUSER, GMAILPASSWORD)
        smtp_server.sendmail(GMAILUSER, EMAILLIST, emailText)
        smtp_server.close()
    except Exception as error:
        print('**Error sending low water email: ', error)

def notifyWaterFilled(currentTime):
    subject = 'ROOT ACCESS: Your water resevoir has been refilled'
    date = time.localtime(currentTime)
    localDate = time.asctime(date)
    body = f'Thank you for refilling your Root Access resevoir at {localDate}. Your plant may now continue to grow and bloom'
    emailText = '''\n
    From: %s
    To: %s
    Subject: %s

    %s
    '''%(GMAILUSER, EMAILLIST, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(GMAILUSER, GMAILPASSWORD)
        smtp_server.sendmail(GMAILUSER, EMAILLIST, emailText)
        smtp_server.close()
    except Exception as error:
        print('**Error sending filled reservoir email: ', error)

def resetPasswordEmail(email, secret):
    ip = socket.gethostbyname(socket.gethostname())
    redirectUrl = f'{ip}/resetPassword?email={email}ref={secret}'
    subject = 'ROOT ACCESS: Password Reset'
    body = f'Here\'s a link to reset your password! {redirectUrl}'
    emailText = '''\n
    From: %s
    To: %s
    Subject: %s

    %s
    '''%(GMAILUSER, EMAILLIST, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(GMAILUSER, GMAILPASSWORD)
        smtp_server.sendmail(GMAILUSER, EMAILLIST, emailText)
        smtp_server.close()
    except Exception as error:
        print('**Error sending reset password email: ', error)