"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from MxOnline.settings import MEDIA_ROOT
from apps.users.views import IndexViews

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),  # 后台管理系统
    url(r'^$', IndexViews.as_view(), name='index'),  # 主页
    url(r'^captcha/', include('captcha.urls')),  # 页码
    url(r'^up_image/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 图片保存路径
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}), # DEBUG 静态文件地址

    url(r'^courses/', include('xcourses.urls', namespace='courses')),  # 课程
    url(r'^org/', include('organization.urls', namespace='org')),  # 机构
    url(r'^usercenter/', include('operation.urls', namespace='usercenter')),  # 信息中心
    url(r'^user/', include('users.urls', namespace='user')),  # 用户
]

# handler404 = 'users.views.page_not_found'
# handler500 = 'users.views.page_errorpyt'