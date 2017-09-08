from django.conf.urls import url

from .views import *
urlpatterns = [
    url(r'^list/$', CourseListViews.as_view(),name='list'),
    url(r'^detail/(?P<course_id>.*)/$', CourseDtailViews.as_view(), name='detail'),
    url(r'^video/(?P<course_id>.*)/$', CourseVideoViews.as_view(), name='video'),
    url(r'^comment/(?P<course_id>.*)/$', CourseCommentViews.as_view(), name='comment'),
    url(r'^add_comment/$', AddCommentViews.as_view(), name='add_comment'),
    url(r'^play/(?P<video_id>.*)/$', CoursePlayViews.as_view(), name='play'),
]