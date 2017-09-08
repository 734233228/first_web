from django import forms
import re

import operation.models

class UserAskForm(forms.ModelForm):
    """
    my_filed = forms.CharField() 可以自定义字段
    """
    class Meta:
        model = operation.models.UserAsk
        fields = ['name', 'mobile', 'course_name']
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        RE_MOBILE = "^1[358]\d{9}$|^147\d{8}|^176\d{8}$"
        p = re.compile(RE_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code='mobile_invalid')


class UpLoadImageForm(forms.ModelForm):
    class Meta:
        model = operation.models.UsersProfile
        fields = ['image']


class SaveUserCenterForm(forms.ModelForm):
    class Meta:
        model = operation.models.UsersProfile
        fields = ['nick_name','birthday', 'gander', 'address', 'mobile']

