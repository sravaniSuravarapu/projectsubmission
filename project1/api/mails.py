from django.core.mail import send_mail
from project1.settings import EMAIL_HOST_PASSWORD
import smtplib
from .logs import logger

sender = 'dseo2k22@gmail.com'

def send_verify_mail(url, recipient):
    url = 'Hi, \n\n Please find verification url below\n\n' + url
    print(EMAIL_HOST_PASSWORD)
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com: 587')
        smtpObj.starttls()
        smtpObj.login(sender, EMAIL_HOST_PASSWORD)
        smtpObj.sendmail(sender, recipient, url)
        # smtpObj.quit()
    except Exception as e:
        logger.error(e)

def send_password_mail(url, recipient):
    url = 'Hi, \n\n Please find password reset url below\n\n' + url
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com: 587')
        smtpObj.starttls()
        smtpObj.login(sender, EMAIL_HOST_PASSWORD)
        smtpObj.sendmail(sender, recipient, url)
        # smtpObj.quit()
    except Exception as e:
        logger.error(e)




# def send_verify_mail(url, recipient):
#     url = 'Hi, \n\n Please find verification url below\n\n' + url
#     try:
#         send_mail(
#             'Verification mail for sign-up',
#             url,
#             'dseo2k22@gmail.com',
#             [recipient],
#             fail_silently=False
#         )
#     except Exception as e:
#         logger.error(e)

# def send_password_mail(url, recipient):
#     url = 'Hi, \n\n Please find password reset url below\n\n' + url
#     try:
#         send_mail(
#             'Password reset mail',
#             url,
#             'dseo2k22@gmail.com',
#             [recipient],
#             fail_silently=False
#         )
#     except Exception as e:
#         logger.error(e)