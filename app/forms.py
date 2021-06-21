from django.forms import ModelForm, Textarea, SelectMultiple
from django.utils.translation import gettext_lazy as _

from app.models import Question, Answer


class AskForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'text', 'tag')
        labels = {
            'title': _('Title'),
            'text': _('Text'),
            'tag': _('Tags')
        }
        widgets = {
            'title': Textarea(attrs={
                'placeholder': 'How to a build a moon park?',
                'rows': 1,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'text': Textarea(attrs={
                'placeholder': 'Really?\nHow? Have no idea about it',
                'rows': 12,
                'style': 'width: 100%;',
                'class': 'form-control'
            }),
            'tag': SelectMultiple(attrs={
                'rows': 12,
                'style': 'width: 100%; height: 300px;',
                'class': 'form-control'
            })
        }


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('text', )
        labels = {
            'text': _('Your answer')
        }
        widgets = {
            'text': Textarea(attrs={
                'placeholder': 'Enter your answer here...',
                'rows': 3,
                'style': 'width: 100%;',
                'class': 'form-control'
            })
        }
