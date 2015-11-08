# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from my_auth.models import MyUser


class MyLoginForm(AuthenticationForm):

    username = forms.CharField(label=_('username'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-7'

        self.helper.add_input(Submit('submit', 'Login',
                                     css_class='btn btn-default btn-md col-md-offset-5'))

        self.helper.layout = Layout(
            Field(
                'username', placeholder='Input your login'
            ),
            Field(
                'password', placeholder='Input your password'
            )
        )


class MyRegForm(UserCreationForm):
    form_name = 'reg_form'
    error_messages = {
        'password_mismatch': "Passwords mismatch",
    }
    username = forms.CharField(label=_('Id no'), help_text='Max 30 characters')
    password1 = forms.CharField(min_length=6, label=_('password'), widget=forms.PasswordInput,
                                help_text=_("Min 6 characters"))
    password2 = forms.CharField(min_length=6, label=_('password again'),
                                widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=50, label=_('last name'))
    first_name = forms.CharField(max_length=50, label=_('first name'))
    email = forms.EmailField(label=_('Email Address'), required=True,)

    def __init__(self, *args, **kwargs):
        super(MyRegForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-7'

        self.helper.add_input(Submit('submit', _('Sign Up'),
                                     css_class='btn btn-default btn-md col-md-offset-5'))

        self.helper.layout = Layout(
            Field(
                'username', placeholder='Id no'
            ),
            Field(
                'password', placeholder='Password'
            ),
            Field(
                'email', placeholder='Email Address'
            )
        )

    class Meta:
        model = MyUser
        fields = ('last_name', 'first_name', 'username',
                  'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(MyRegForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
