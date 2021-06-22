import json

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from app.forms import AskForm, AnswerForm, SignUpForm, SignInForm, UserSettingsForm
from app.models import Question, Tag, Answer, User, LikeQuestions


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


class ToggleAnswerIsCorrect(LoginRequiredMixin, View):
    """Пометка ответа как правильного или нет"""

    def post(self, request, pk):
        try:
            answer = get_object_or_404(Answer, pk=pk)
        except Answer.DoesNotExist:
            return JsonResponse({'success': False, 'reason': 'Answer doesn\'t exist'}, status=404)
        try:
            question = get_object_or_404(Question, pk=answer.question_id)
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'reason': 'Question doesn\'t exist'}, status=404)
        if question.author != request.user.user:
            return JsonResponse({'success': False, 'reason': ''})

        if answer.is_correct:
            answer.is_correct = False
        else:
            previous_correct_answer = Answer.objects.get_correct_answers(answer.question_id)
            for a in previous_correct_answer:
                a.is_correct = False
                a.save()
            answer.is_correct = True
        answer.save()

        return JsonResponse({'success': True})


class AskView(LoginRequiredMixin, View):
    """Создание нового вопроса"""

    def get(self, request):
        form = AskForm()
        return render(request, 'ask.html', {'form': form})

    def post(self, request):
        form = AskForm(request.POST)
        if not form.is_valid():
            return render(request, 'ask.html', {'form': form})
        new_question = form.save(commit=False)
        new_question.author = request.user.user
        new_question.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('question', args=(new_question.id, )))


class HotView(View):
    """Список “лучших” вопросов"""

    def get(self, request):
        context = paginate(Question.objects.get_hottest(
            request.user.user.id if request.user.is_authenticated else None
        ), request, 3)
        return render(request, 'hot_questions.html', context)


class ListingQView(View):
    """Список вопросов по тегу"""

    def get(self, request, tag_name):
        context = paginate(Question.objects.get_by_tag(
            tag_name,
            request.user.user.id if request.user.is_authenticated else None
        ), request, 3)
        context['tags'] = Tag.objects.get_by_text(tag_name)
        return render(request, 'listing_q.html', context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))

        form = SignInForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.POST.get('next') or reverse('main')
            return HttpResponseRedirect(next)
        else:
            form = SignInForm()
            return render(request, 'login.html', {'form': form, 'unauthorized': True})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main'))


class QuestionLikeView(LoginRequiredMixin, View):
    """Обработка лайка/дизлайка"""

    def post(self, request, pk):
        try:
            q = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'reason': 'Question doesn\'t exist'}, status=404)

        request_body = request.body.decode('utf-8')
        body = json.loads(request_body)
        if 'mark' not in body or not isinstance(body.get('mark'), int) or not body.get('mark') in [1, -1]:
            return JsonResponse({'success': False, 'reason': 'Invalid body'}, status=400)

        try:
            like = LikeQuestions.objects.get(question=q, user=request.user.user)
        except LikeQuestions.DoesNotExist:
            like = LikeQuestions.objects.create(
                question=q,
                user=request.user.user,
                mark=body.get('mark')
            )
            return JsonResponse({'success': True, 'mark': like.mark})

        if body.get('mark') == 1:
            if like.mark < 1:
                like.mark += 1
                like.save()
        elif body.get('mark') == -1:
            if like.mark > -1:
                like.mark -= 1
                like.save()

        return JsonResponse({'success': True, 'mark': like.mark})


class QuestionView(View):
    """Страница 1 вопроса со списком ответов"""

    def get(self, request, pk):
        q = Question.objects.get_one(
            pk,
            request.user.user.id if request.user.is_authenticated else None
        )
        if len(q) == 0:
            raise Http404('Question doesn\'t found')
        context = paginate(Answer.objects.get_by_question(pk), request, 3)
        context['question'] = q[0]
        context['form'] = AnswerForm()
        return render(request, 'question.html', context)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        form = AnswerForm(request.POST)
        if not form.is_valid():
            return render(request, 'question.html', {'form': form})
        new_answer = form.save(commit=False)
        new_answer.author = request.user.user
        new_answer.question_id = pk
        new_answer.save()
        return HttpResponseRedirect(reverse('question', args=(pk, )))


class SettingsView(LoginRequiredMixin, View):
    """Настройки пользователя"""

    def get(self, request):
        form = UserSettingsForm(instance=request.user)
        return render(request, 'settings.html', {'form': form})

    def post(self, request):
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if not form.is_valid():
            return render(request, 'settings.html', {'form': form})
        user = request.user.user
        user.image = form.cleaned_data.get('image')
        user.save()
        form.save()
        return HttpResponseRedirect(reverse('settings'))


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))

        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))

        form = SignUpForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})
        new_django_user = form.save()
        new_user = User.objects.create(
            django_user=new_django_user,
            image=form.cleaned_data.get('image')
        )
        new_user.save()
        return HttpResponseRedirect(reverse('login'))


class IndexView(View):
    """Список новых вопросов"""

    def get(self, request):
        context = paginate(Question.objects.get_latest(
            request.user.user.id if request.user.is_authenticated else None
        ), request, 3)
        return render(request, 'index.html', context)
