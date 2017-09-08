from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class UsersProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gander = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image_download/%Y/%m", default=u"", )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_usermessage(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVeritfyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register', u'注册'), ('forget', u'找回密码'), ('upload', u'更改邮箱')), max_length=10,
                                 verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner_download/%Y/&m', verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
