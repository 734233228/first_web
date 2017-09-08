import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin:
    list_display = ['name', 'desc', 'add_times']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_times']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'org_type', 'click_nums', 'fav_nums', 'address', 'city', 'add_times']
    search_fields = ['name', 'desc', 'org_type', 'click_nums', 'fav_nums', 'address', 'city__name']
    list_filter = ['name', 'desc', 'org_type', 'click_nums', 'fav_nums', 'address', 'city__name','add_times']


class TeacherAdmin:
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                    'add_times']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                   'add_times']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
