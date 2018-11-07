import time
import datetime
import json
from django.core.mail import send_mail,EmailMultiAlternatives
from . import settings

def addCurrentTime(dic):
    dic['createdate'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    dic['updatedate'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
   # print('时间：'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return dic

if __name__=="__main__":
    print('当前时间：{0}'.format(datetime.datetime.now()))

class MailUtil(object):
    url = 'http://127.0.0.1:8000/active_acct/'

    def __init__(self):
        pass

    #用户注册验证邮件,通过链接中的邮箱确认
    @classmethod
    def send_register_email(cls,email_acct,userid):
        subject = 'NoteAndShare用户注册<www.freej.top>'
        msg = '点击此链接完成注册：<a href="'+cls.url+email_acct+'/">确认</a>'
        to_list = [email_acct,]

        mail = EmailMultiAlternatives(subject,msg,settings.EMAIL_HOST_USER,to_list)
        mail.content_subtype = 'html'
        mail.send()

class JsonUtil(object):
    @staticmethod
    def get_json_response(result,msg):
        return json.dumps({'result':result,'msg':msg})

