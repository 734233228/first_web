from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^logout/$', LogoutViews.as_view(), name='logout'),
    url(r'^login/$', LoginViews.as_view(), name='login'),
    url(r'^register/$', RegisterViews.as_view(), name='register'),
    url(r'^forgetpwd/$', ForgetViews.as_view(), name='forgetpwd'),
    url(r'^password_form/$', ResetPwdFormViews.as_view(), name='password_form'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserViews.as_view(), name='active'),
    url(r'^password_reset/(?P<active_code>.*)/$', ResetPwdViews.as_view(), name='resetpwd'),
]
