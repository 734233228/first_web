from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^info/$', UserCenterInfoViews.as_view(), name='info'),
    url(r'^mycourse/$', UserCenterMyCourseViews.as_view(), name='mycourse'),
    url(r'^message/$', UserCenterMessageViews.as_view(), name='message'),
    url(r'^fav_course/$', UserCenterFavCourseViews.as_view(), name='fav_course'),
    url(r'^fav_org/$', UserCenterFavOrgViews.as_view(), name='fav_org'),
    url(r'^fav_teacher/$', UserCenterFavTeacherViews.as_view(), name='fav_teacher'),
    url(r'^uploadiamge/$', UpLoadImageViews.as_view(), name='up_load_image'),
    url(r'^uppwd/$', UpPwdViews.as_view(), name='up_pwd'),
    url(r'^sendemailcode/$', UpLoadEmailView.as_view(), name='send_email_code'),
    url(r'^add_ask_form/$', AddAskViews.as_view(), name="add_ask_form"),
]
