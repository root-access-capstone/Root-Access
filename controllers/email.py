import smtplib
import time
import socket
gmailUser = 'rootaccesplant@gmail.com'
gmailPassword = 'rootaccess2022'

emailList = ['leaderfirestar@ksu.edu', 'jrmartin@ksu.edu', 'aquariuswre@ksu.edu']

def notifyLowWater(currentTime):
    subject = 'Your plant needs water'
    date = time.localtime(currentTime)
    localDate = time.asctime(date)
    body = f'Attention Users! The water levels in your system are low as of {localDate}, and it needs to be refilled'
    emailText = '''\n
    From: %s
    To: %s
    Subject: %s

    %s
    '''%(gmailUser, emailList, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmailUser, gmailPassword)
        smtp_server.sendmail(gmailUser, emailList, emailText)
        smtp_server.close()
    except Exception as e:
        print('Uh oh. There was a fucky wucky while sending the email')
        print(e)

def notifyWaterFilled(currentTime):
    subject = 'Your water resevoir has been refilled'
    date = time.localtime(currentTime)
    localDate = time.asctime(date)
    body = f'Thank you for refilling your Root Access resevoir at {localDate}. Your plant may now continue to grow and bloom'
    emailText = '''\n
    From: %s
    To: %s
    Subject: %s

    %s
    '''%(gmailUser, emailList, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmailUser, gmailPassword)
        smtp_server.sendmail(gmailUser, emailList, emailText)
        smtp_server.close()
    except Exception as e:
        print('Uh oh. There was a fucky wucky while sending the email')
        print(e)

def resetPasswordEmail(email, secret):
    ip = socket.gethostbyname(socket.gethostname())
    redirectUrl = f'{ip}/resetPassword?email={email}ref={secret}'
    subject = 'Password Reset'
    body = f'Here\'s a link to reset your password! {redirectUrl}'
    emailText = '''\n
    From: %s
    To: %s
    Subject: %s

    %s
    '''%(gmailUser, emailList, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmailUser, gmailPassword)
        smtp_server.sendmail(gmailUser, emailList, emailText)
        smtp_server.close()
    except Exception as e:
        print('Uh oh. There was a fucky wucky while sending the email')
        print(e)