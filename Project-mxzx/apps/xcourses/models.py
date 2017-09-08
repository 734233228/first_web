from django.db import models
from datetime import datetime

from organization.models import CourseOrg, Teacher

# Create your models here.3


class Course(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True)
    teacher = models.ForeignKey(Teacher, verbose_name='授课讲师', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2, verbose_name=u'难度', default='cj')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course_download/%Y/%m', verbose_name=u'封面')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(default=u'后端开发', verbose_name=u'学习方向', max_length=20)
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    tag = models.CharField(default=u'', verbose_name=u'标签', max_length=20)
    procla = models.CharField(default=u'', verbose_name=u'课程公告', max_length=100)
    teacher_talks = models.CharField(default=u'', verbose_name=u'老师心得', max_length=300)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    def learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_lesson(self):
        return self.lesson_set.all()

    def get_resource(self):
        return self.courseresource_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url_address = models.CharField(verbose_name=u'视频地址', max_length=200, default='')
    learn_times = models.CharField(verbose_name=u'小节视频长度', max_length=8, default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名称')
    name = models.CharField(max_length=100, verbose_name=u'课程资源')
    download = models.FileField(upload_to='course_download/resource/%Y/%m', verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
