from django.conf.urls import url

from .views import *
urlpatterns = [
    url(r'^list/$',OrgListViews.as_view(),name='list'),
    url(r'^home/(?P<org_id>.*)/$', OrgHomeViews.as_view(), name='home'),
    url(r'^course/(?P<org_id>.*)/$', OrgCourseViews.as_view(), name='course'),
    url(r'^decs/(?P<org_id>.*)/$', OrgDecsViews.as_view(), name='decs'),
    url(r'^teather/(?P<org_id>.*)/$', OrgTeacherViews.as_view(), name='teacher'),
    url(r'^fav/$', OrgFavViews.as_view(), name='fav'),
    url(r'^teacher_detail/(?P<teacher_id>.*)/$', TeacherDetailViews.as_view(), name='teacher_detail'),
    url(r'^teacher_list/$', TeacherListViews.as_view(), name='teacher_list'),
]