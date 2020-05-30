from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )


class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description',
                  'city',
                  'state',
                  'phone',
                  'image'
                  )
'''
class HomeForm(forms.Form):
    name=forms.CharField()
    standard=forms.CharField()
'''
