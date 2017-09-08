from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Course, Video
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin import LoginRequiredMixin
# Create your views here.


class CourseListViews(View):
    def get(self,request):
        name = 'course'
        all_course = Course.objects.all().order_by("-add_time")
        sort = request.GET.get("sort", '')
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = Course.objects.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                               Q(detail__icontains=search_keywords))

        if sort:
            if sort == 'hot':
                all_course = Course.objects.all().order_by("-click_nums")
            elif sort == 'students':
                all_course = Course.objects.all().order_by("-students")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 3, request=request)
        all_course_page = p.page(page)
        return render(request, 'course_list.html', {"name": name, 'all_course_page': all_course_page, 'sort': sort})


class CourseDtailViews(View):
    def get(self, request, course_id):
        name = 'course'
        is_fav_course = False
        is_fav_org = False
        course = Course.objects.get(id=int(course_id))
        if request.user.is_authenticated():
            fav_course = UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id)
            fav_org = UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.org.id)
            if fav_course:
                is_fav_course = True
            if fav_org:
                is_fav_org = True
        # 课程点击数
        course.click_nums += 1
        course.save()

        # 相关课程推荐
        if course.tag:
            all_tag = Course.objects.filter(tag=course.tag)[:3]
        else:
            all_tag = []
        return render(request, 'course_detail.html', {"course": course, 'all_tag': all_tag,
                                                      'is_fav_course': is_fav_course,
                                                      'is_fav_org': is_fav_org,
                                                      'name': name
                                                      })


class CourseVideoViews(LoginRequiredMixin, View):
    def get(self, request, course_id):
        name = 'course'
        # 课程点击数自加1
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 添加该门课程到 UserCourse 中
        add_user_course = UserCourse.objects.filter(user=request.user, course=int(course_id))
        if not add_user_course:
            UserCourse.objects.create(user=request.user, course=course)
        # 学过该课程的同学还学过什么课程，热度排序
        filter_user_course = UserCourse.objects.filter(course=course)  # 通过 课程 在UserCourse中筛选
        user_id = [user_id.user.id for user_id in filter_user_course]  # 通过遍历获取到所有用户的user.id
        user_course = UserCourse.objects.filter(user_id__in=user_id)  # 通过 用户id 在UserCourse中筛选
        course_id = [course_id.course.id for course_id in user_course]  # 遍历获取课程id
        all_course = Course.objects.filter(id__in=course_id).order_by('-click_nums')[:5]
        return render(request, 'course_video.html', {'name': name, 'course': course, 'all_course': all_course})


class CourseCommentViews(LoginRequiredMixin, View):
    def get(self, request, course_id):
        name = 'course'
        course = Course.objects.get(id=int(course_id))
        all_comment = CourseComment.objects.all()
        return render(request, 'course_comment.html', {'name': name, 'course': course, 'all_comment': all_comment})


class AddCommentViews(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comment = request.POST.get("comments", "")
        if int(course_id) > 0 and comment:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComment()
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comment = comment
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"出现了很意外的事故"}', content_type='application/json')


class CoursePlayViews(View):
     def get(self, request, video_id):
        name = 'course'
        # 课程点击数自加1
        video_id = Video.objects.get(id=video_id)
        course = Course.objects.get(lesson__video=video_id)
        course.students += 1
        course.save()
        # 学过该课程的同学还学过什么课程，热度排序
        filter_user_course = UserCourse.objects.filter(course=course)  # 通过 课程 在UserCourse中筛选
        user_id = [user_id.user.id for user_id in filter_user_course]  # 通过遍历获取到所有用户的user.id
        user_course = UserCourse.objects.filter(user_id__in=user_id)  # 通过 用户id 在UserCourse中筛选
        course_id = [course_id.course.id for course_id in user_course]  # 遍历获取课程id
        all_course = Course.objects.filter(id__in=course_id).order_by('-click_nums')[:5]
        return render(request, 'course-play.html', {'name': name, 'course': course, 'all_course': all_course,
                                                    'video_id': video_id})
