import random

from django.contrib.auth.models import User as DjangoUser
from django.core.management.base import BaseCommand
from app.models import Question, User, Tag, Answer, LikeQuestions
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fill_users(options['users'])
        self.fill_tags(options['tags'])
        self.fill_questions(options['questions'])
        self.fill_answers(options['answers'])
        self.fill_likes(options['likes'])

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            action='store',
            dest='users',
            type=int
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store',
            dest='tags',
            type=int
        )
        parser.add_argument(
            '-q',
            '--questions',
            action='store',
            dest='questions',
            type=int
        )
        parser.add_argument(
            '-a',
            '--answers',
            action='store',
            dest='answers',
            type=int
        )
        parser.add_argument(
            '-l',
            '--likes',
            action='store',
            dest='likes',
            type=int
        )

    def fill_users(self, cnt):
        for i in range(cnt):
            du = DjangoUser.objects.create(
                username=f.user_name(),
                first_name=f.first_name(),
                last_name=f.last_name(),
                email=f.email()
            )
            if i % 3 == 0:
                avatar = 'auto.jpg'
            elif i % 2 == 0:
                avatar = 'moto.jpg'
            else:
                avatar = None
            User.objects.create(
                django_user=du,
                image=avatar
            )

    def fill_tags(self, cnt):
        for i in range(cnt):
            Tag.objects.create(
                text=f.word()
            )

    def fill_questions(self, cnt):
        users_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        tags_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            qst = Question.objects.create(
                author_id=choice(users_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:128],
                created=f.date_time()
            )
            for i in range(f.random_int(min=0, max=15)):
                qst.tag.add(tags_ids[f.random_int(min=0, max=len(tags_ids)-1)])

    def fill_answers(self, cnt):
        users_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        qst_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Answer.objects.create(
                author_id=choice(users_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                question_id=choice(qst_ids)
            )

    def fill_likes(selfself, cnt):
        users_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        qst_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        likes = set()
        for i in range(cnt):
            before_len = len(likes)
            len_diff = 0
            while len_diff == 0:
                likes.add((choice(users_ids), choice(qst_ids)))
                len_diff = len(likes) - before_len

        for like in likes:
            LikeQuestions.objects.create(
                user_id=like[0],
                question_id=like[1],
                mark=choice([-1, 1])
            )
