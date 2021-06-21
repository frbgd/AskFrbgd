from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from app.forms import AskForm, AnswerForm, SignUpForm
from app.models import Question, Tag, Answer, User


def paginate(objects_list, request, per_page):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return context


def error_404(request, exception):
    return render(request, '404.html', {})


class AskView(View):
    def get(self, request):
        form = AskForm()
        return render(request, 'ask.html', {'form': form})

    def post(self, request):
        form = AskForm(request.POST)
        new_question = form.save(commit=False)
        new_question.author_id = 1  # TODO set current user
        new_question.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('question', args=(new_question.id, )))


def hot(request):
    """Список “лучших” вопросов"""
    context = paginate(Question.objects.get_hottest(), request, 3)
    return render(request, 'hot_questions.html', context)


def listing_q(request, tag_name):
    """Список вопросов по тегу"""
    context = paginate(Question.objects.get_by_tag(tag_name), request, 3)
    context['tags'] = Tag.objects.get_by_text(tag_name)
    return render(request, 'listing_q.html', context)


def login(request):
    return render(request, 'login.html', {})


class QuestionView(View):
    """Страница 1 вопроса со списком ответов"""

    def get(self, request, pk):
        q = get_object_or_404(Question, pk=pk)
        context = paginate(Answer.objects.get_by_question(pk), request, 3)
        context['question'] = q
        context['form'] = AnswerForm()
        return render(request, 'question.html', context)

    def post(self, request, pk):
        form = AnswerForm(request.POST)
        new_answer = form.save(commit=False)
        new_answer.author_id = 1  # TODO set current user
        new_answer.question_id = pk
        new_answer.save()
        return HttpResponseRedirect(reverse('question', args=(pk, )))


def settings(request):
    return render(request, 'settings.html', {})


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})
        new_django_user = form.save()
        new_user = User.objects.create(
            django_user=new_django_user
        )
        new_user.save()
        return HttpResponseRedirect(reverse('main'))


def index(request):
    """Список новых вопросов"""
    context = paginate(Question.objects.get_latest(), request, 3)
    return render(request, 'index.html', context)
