from django.shortcuts import render,HttpResponse
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
import json
from .forms import UserAskForm, UpLoadImageForm,SaveUserCenterForm
from utils.mixin import LoginRequiredMixin
from users.forms import PwdForm
from utils import email_send
from users.models import UsersProfile, EmailVeritfyRecord
from operation.models import UserCourse, UserFavorite, UserMessage
from xcourses.models import Course
from organization.models import CourseOrg, Teacher
# Create your views here.


class AddAskViews(View):
    """
    用户添加咨询
    """
    def post(self,request):
        user_ask_form = UserAskForm(request.POST,)
        if user_ask_form.is_valid():
            user_ask_form.save()
            return HttpResponse('{"status": "success"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg":"输入非法"}', content_type="application/json")


class UserCenterInfoViews(LoginRequiredMixin, View):
    """
    个人中心_个人信息
    """
    def get(self,request):
        return render(request, 'usercenter_info.html')

    # 个人信息保存提交
    def post(self,request):
        save_user_center_form = SaveUserCenterForm(request.POST, instance=request.user)
        if save_user_center_form.is_valid():
            save_user_center_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            a = json.dumps(save_user_center_form.errors)
            return HttpResponse(json.dumps(save_user_center_form.errors), content_type="application/json")


class UserCenterMyCourseViews(LoginRequiredMixin, View):
    """
    个人中心_我的课程
    """
    def get(self, request):
        all_fav_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter_mycourse.html',{'all_fav_courses': all_fav_courses})


class UserCenterMessageViews(LoginRequiredMixin, View):
    """
    个人中心_我的消息
    """
    def get(self, request):
        user_message = UserMessage.objects.filter(user=request.user.id)
        for message in user_message:
            message.has_read = True
            message.save()
        return render(request, 'usercenter_message.html', {"user_message":user_message})


class UserCenterFavCourseViews(LoginRequiredMixin, View):
    """
    个人中心_我收藏的课程
    """
    def get(self, request):
        user_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        courses_id = [course_id.fav_id for course_id in user_courses]
        all_courses = Course.objects.filter(id__in=courses_id)
        return render(request, 'usercenter_fav_course.html', {"all_courses": all_courses})

    # 机构、课程、讲师收藏的删除
    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')
        delete_fav = UserFavorite.objects.get(user=request.user, fav_id=int(fav_id),fav_type=int(fav_type))
        if delete_fav:
            delete_fav.delete()
            return HttpResponse('{"status":"删除成功"}', content_type="application/json")


class UserCenterFavOrgViews(LoginRequiredMixin, View):
    """
    个人中心_我收藏的机构
    """
    def get(self, request):
        user_org = UserFavorite.objects.filter(user=request.user, fav_type=2)
        org_id = [org_id.fav_id for org_id in user_org]
        all_org = CourseOrg.objects.filter(id__in=org_id)
        return render(request, 'usercenter_fav_org.html', {"all_org":all_org})


class UserCenterFavTeacherViews(LoginRequiredMixin, View):
    """
    个人中心_我收藏的讲师
    """
    def get(self, request):
        user_teacher = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teachers_id = [teachers_id.fav_id for teachers_id in user_teacher]
        all_teachers = Teacher.objects.filter(id__in=teachers_id)
        return render(request, 'usercenter_fav_teacher.html', {"all_teachers": all_teachers})


class UpLoadImageViews(LoginRequiredMixin, View):
    """
    个人中心_个人信息_图片上传
    """
    def post(self,request):
        upimage_form = UpLoadImageForm(request.POST, request.FILES, instance=request.user)
        if upimage_form.is_valid():
            request.user.save()
        else:
            pass


class UpPwdViews(LoginRequiredMixin, View):
    """
    个人中心_个人信息_密码修改
    """
    def post(self, request):
        pwd_form = PwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 == pwd2:
                user = request.user
                user.password = make_password(pwd1)
                user.save()
                return HttpResponse('{"status":"success"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"两次输入不一致"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(pwd_form.errors), content_type="application/json")


class UpLoadEmailView(LoginRequiredMixin, View):
    """
    个人中心邮箱更改
    """
    # 获取验证码
    def get(self, request):
        email = request.GET.get('email', '')
        if UsersProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已注册"}', content_type="application/json")
        email_send.send_register_email(email, 'upload')
        return HttpResponse('{"status":"success"}', content_type="application/json")

    # 更改邮箱
    def post(self, request):
        email = request.POST.get('email','')
        code = request.POST.get('code', '')
        if EmailVeritfyRecord.objects.filter(email=email, code=code, send_type='upload'):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        return HttpResponse('{"email":"验证码不正确"}', content_type="application/json")
