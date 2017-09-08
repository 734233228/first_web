from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from operation.models import UserFavorite
from organization.models import CourseOrg, CityDict, Teacher
from xcourses.models import Course
# Create your views here.


class OrgListViews(View):
    """
    机构列表页
    """
    def get(self, request):
        name = 'org'
        all_org = CourseOrg.objects.all()
        hot_org = CourseOrg.objects.all().order_by('fav_nums')[:3]
        all_city = CityDict.objects.all()
        city_id = request.GET.get('city_id', '')
        org_type = request.GET.get('org_type', '')
        sort = request.GET.get('sort', '')
        search_keywords = request.GET.get('keywords', '')
        # 全局搜索
        if search_keywords:
            all_org = CourseOrg.objects.filter(Q(name__icontains=search_keywords)
                                                 | Q(desc__icontains=search_keywords)
                                                 | Q(org_type__icontains=search_keywords)
                                               )
        # 城市、机构类型联合筛选
        if org_type and city_id:
            all_org = CourseOrg.objects.filter(org_type=org_type, city_id=int(city_id))
        elif org_type:
            all_org = CourseOrg.objects.filter(org_type=org_type,)
        elif city_id:
            all_org = CourseOrg.objects.filter(city_id=int(city_id))

        # 筛选后的结果进行学习认输或课程数进行排序
        if sort:
            all_org = all_org.order_by('-'+sort)

        #页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, 5, request=request)
        all_org_page = p.page(page)
        org_num = all_org.count()
        return  render(request, 'org_list.html', {'all_org_page': all_org_page,
                                                  'all_city': all_city,
                                                  'city_id': city_id,
                                                  'org_type': org_type,
                                                  'org_num': org_num,
                                                  'sort': sort,
                                                  'name': name,
                                                  'hot_org': hot_org

                                                  })


class OrgHomeViews(View):
    def get(self, request, org_id):
        current_page = 'home'
        corese_org = CourseOrg.objects.get(id=int(org_id))
        is_fav = False
        if request.user.is_authenticated():
            fav = UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=int(org_id))
            if fav:
                is_fav = True
        return render(request, 'org_home.html', {"corese_org": corese_org, "current_page": current_page, 'is_fav': is_fav})


class OrgCourseViews(View):
    def get(self, request, org_id):
        current_page = 'course'
        corese_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org_course.html',{"current_page":current_page,"corese_org": corese_org})



class OrgDecsViews(View):
    """
    机构介绍页码
    """
    def get(self, request, org_id):
        current_page = 'decs'
        corese_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org_decs.html', {"current_page":current_page,"corese_org": corese_org,})


class OrgTeacherViews(View):
    """
    机构讲师页面
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        corese_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org_teather.html', {"current_page":current_page, "corese_org": corese_org,})


class OrgFavViews(View):
    """
    用户收藏及取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',  content_type="application/json")
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            # 相应的收藏减1
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            if int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"fail", "msg":"收藏已删除"}', content_type="application/json")
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                # 相应的收藏加1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                if int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}' ,content_type="application/json")


class TeacherListViews(View):
    """
    讲师列表页面
    """
    def get(self,request):
        name = 'teacher'
        all_teacher = Teacher.objects.all().order_by('-add_times')
        sort = request.GET.get("sort", '')
        search_keywords = request.GET.get('keywords', '')
        # 全局搜索
        if search_keywords:
            all_teacher = Teacher.objects.filter(Q(name__icontains=search_keywords)
                                                 | Q(work_position__icontains=search_keywords)
                                                 | Q(points__icontains=search_keywords)
                                                 | Q(work_company__icontains=search_keywords)
                                                 )
        # 按点击数排列
        if sort:
            all_teacher = Teacher.objects.all().order_by('-click_nums')
        search_keywords = request.GET.get('keywords', '')

        # 讲师排行榜 按收藏数排列只取3个
        fav_teacher = Teacher.objects.all().order_by('-fav_nums')[:3]

        # 生成页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 5, request=request)
        all_teacher_page = p.page(page)

        return render(request, 'teachers_list.html',{"name": name, 'all_teacher': all_teacher_page, 'sort': sort,
                                                     "fav_teacher": fav_teacher
                                                     })

class TeacherDetailViews(View):
    """
    老师详细页面
    """
    def get(self, request, teacher_id):
        name = 'teacher'
        teacher_obj = Teacher.objects.get(pk=int(teacher_id))

        # 老师点击数自加1
        teacher_obj.click_nums += 1
        teacher_obj.save()

        # 老师排行榜 只取收藏数最多的3名老师
        hot_teacher = Teacher.objects.all().order_by('-fav_nums')[:3]

        # 判断用户是否收藏了老师或机构
        is_teacher_fav = False
        is_org_fav = False
        if request.user.is_authenticated():
            teacher_fav = UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=int(teacher_id))
            org_fav = UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher_obj.org.id)
            if teacher_fav:
                is_teacher_fav = True
            if org_fav:
                is_org_fav = True

        return render(request, 'teacher_detail.html', {'name':name, 'teacher_obj': teacher_obj,
                                                       'hot_teacher': hot_teacher,
                                                       'is_teacher_fav': is_teacher_fav,
                                                       'is_org_fav': is_org_fav
                                                       })
