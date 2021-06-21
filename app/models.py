from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import UserManager
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img')
    birth_date = models.DateField()
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class QuestionManager(models.Manager):
    def get_latest(self):
        return self.all().order_by('-created')

    def get_hottest(self):
        return self.raw("""
        SELECT 
        count(lq.user_id) AS likes_cnt, 
        * 
        FROM app_question q
        LEFT JOIN app_likequestions lq 
        ON q.id = lq.question_id 
        GROUP BY lq.question_id 
        ORDER BY likes_cnt DESC;
        """)

    def get_by_tag(self, tag_text):
        return self.filter(tag__text=tag_text)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    created = models.DateTimeField(default=timezone.now)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def get_by_question(self, question_id):
        return self.filter(question_id=question_id)


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    objects = AnswerManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answer'


class TagManager(models.Manager):
    def get_by_text(self, text):
        return self.filter(text=text)[:1]


class Tag(models.Model):
    text = models.CharField(max_length=255)

    objects = TagManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class LikeQuestions(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['question', 'user']
