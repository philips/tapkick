from django import forms
from django.conf import settings
from django.forms.util import ErrorList
from django.core.urlresolvers import reverse
from beer.models import User

class SearchForm(forms.Form):
    user_name = forms.IntegerField()

    def user(self):
        u = User.objects.filter(name = self.cleaned_data["user_name"])
        if u and len(u) == 1:
            return u[0]
        else:
            return False

    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get("user_name")
        user = self.user()

        if (not user):
            msg = u"%s didn't match any or too many users" % name
            self._errors["user_name"] = self.error_class([msg])

        return cleaned_data

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email')
