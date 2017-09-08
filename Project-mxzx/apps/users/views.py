from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

import users.models
from .forms import LoginForm, RegisterForm, ForgetForm, PwdForm
from utils.email_send import send_register_email
from operation.models import UserMessage
from xcourses.models import Course, CourseOrg

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = users.models.UsersProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutViews(View):
    def get(self, request):
        logout(request)
        # return HttpResponseRedirect(reverse('index'))
        return render(request, 'org_list.html')


class LoginViews(View):
    def get(self,request):
        return render(request, 'login.html',)
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))  # 重新定向
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class IndexViews(View):
    def get(self, request):
        banners = users.models.Banner.objects.all().order_by('index')
        course_banners = Course.objects.filter(is_banner=True)
        hot_course = Course.objects.all().order_by('add_time')[:6]
        all_org = CourseOrg.objects.all().order_by('click_nums')[:15]
        return render(request, 'index.html',{'banners': banners, 'course_banners': course_banners, 'hot_course': hot_course, 'all_org':all_org})


class RegisterViews(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            user_profile = users.models.UsersProfile()
            is_register = users.models.UsersProfile.objects.filter(email=user_name, is_active=1)
            if is_register:
                return render(request, 'register.html', {'error': "邮箱已注册"})
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name,send_type='register')
            # 注册成功向用户发送欢迎注册消息
            UserMessage.objects.create(user=user_profile.id, message='欢迎注册慕学网，您的梦想将从这里开始')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form })


class ActiveUserViews(View):
    def get(self, request, active_code):
        all_records = users.models.EmailVeritfyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = users.models.UsersProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')


class ForgetViews(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form': forget_form} )
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email,send_type='forget')
            return render(request, 'forget1.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdViews(View):
    def get(self, request, active_code):
        all_records = users.models.EmailVeritfyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'forget2.html', {'msg': '链接失效'})


class ResetPwdFormViews(View):
    def post(self,request,):
        email = request.POST.get('email', '')
        pwd_form = PwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 == pwd2:
                user = users.models.UsersProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {'email': email, 'msg': "两次密码不一致"})
        else:
            return render(request, 'password_reset.html', {'email': email, 'pwd_form':pwd_form})


def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或者密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})
