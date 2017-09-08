# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'MxOnline.settings'
import random
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM
from users.models import EmailVeritfyRecord

def random_str(code_len=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkRrSsNnOoPpQqRrSsTtUuVvWwXxVvZz123456789'
    chars_lens = len(chars)-1
    code = ''
    for i in range(code_len):
        code += chars[random.randint(0,chars_lens)]
    return code


def send_register_email(email, send_type):
    """
    用户邮箱注册、修改、及密码忘记验证
    
    保存数据，发送验证码到用户邮箱
    """
    code = random_str(20)
    if send_type == 'upload':
        code = random_str(4)
    email_record = EmailVeritfyRecord()
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        email_title = "慕学在线注册激活连接"
        email_body = "请点击下面链接完成激活：http://127.0.0.1:8000/user/active/%s/" % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "慕学在线密码修改链接"
        email_body = "请点击下面链接完成激活：http://127.0.0.1:8000/user/password_reset/%s/" % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'upload':
        email_title = "慕学在线邮箱修改链接"
        email_body = "您的邮箱验证码是：%s" % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


