from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import gettext_lazy as _

from app.models import Question, Answer


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'text', 'tag')
        labels = {
            'title': _('Title'),
            'text': _('Text'),
            'tag': _('Tags')
        }
        widgets = {
            'title': forms.Textarea(attrs={
                'placeholder': 'How to a build a moon park?',
                'rows': 1,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Really?\nHow? Have no idea about it',
                'rows': 12,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'tag': forms.SelectMultiple(attrs={
                'rows': 12,
                'style': 'width: 100%; height: 300px;',
                'class': 'form-control'
            })
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        labels = {
            'text': _('Your answer')
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Enter your answer here...',
                'rows': 3,
                'style': 'width: 100%;',
                'class': 'form-control'
            })
        }


class SignUpForm(UserCreationForm):
    # TODO add Upload avatar field
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': '********',
            'style': 'width: 100%;',
            'class': 'form-control'
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': '********',
            'style': 'width: 100%;',
            'class': 'form-control'
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = DjangoUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.Textarea(attrs={
                'placeholder': 'dr_pepper',
                'rows': 1,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'first_name': forms.Textarea(attrs={
                'placeholder': 'Dr',
                'rows': 1,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'last_name': forms.Textarea(attrs={
                'placeholder': 'Pepper',
                'rows': 1,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'email': forms.Textarea(attrs={
                'placeholder': 'dr.pepper@mail.com',
                'rows': 1,
                'style': 'width: 100%;',
                'class': 'form-control'
            })
        }


class SignInForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'username',
        'style': 'width: 100%;',
        'class': 'form-control'
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': '********',
            'style': 'width: 100%;',
            'class': 'form-control'
        }),
    )
