import time
import datetime
import json
from django.core.mail import send_mail, EmailMultiAlternatives
from expshare import settings, models
import hashlib


def addCurrentTime(dic):
    dic['createdate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    dic['updatedate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print('时间：'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return dic


class MailUtil(object):
    url = 'http://180.76.99.89/active_acct/'

    def __init__(self):
        pass

    # 用户注册验证邮件,通过链接中的邮箱确认
    @classmethod
    def send_register_email(cls, email_acct, user):
        subject = 'NoteAndShare用户注册<www.freej.top>'
        random_code = generate_random_str(email_acct + '-' + str(user.id))
        msg = '点击此链接完成注册：<a href="' + cls.url + str(user.id) + '/' + random_code + '/">确认</a><br/>'
        # msg += '域名备案中，此链接包含IP，若无法打开请直接拷贝此链接粘贴到浏览器中进行激活：'+ cls.url+str(user.id)+'/'+random_code+'/'
        to_list = [email_acct, ]

        dic = {'userid': user, 'code': random_code}
        models.MailRegisterCode.objects.create(**dic)

        mail = EmailMultiAlternatives(subject, msg, settings.EMAIL_HOST_USER, to_list)
        mail.content_subtype = 'html'
        mail.send()


class JsonUtil(object):
    @staticmethod
    def get_json_response(result, msg):
        return json.dumps({'result': result, 'msg': msg})


def generate_random_str(mstr):
    md5 = hashlib.md5()
    md5.update(mstr.encode('utf8'))
    return md5.hexdigest()
