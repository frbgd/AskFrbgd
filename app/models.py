from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import UserManager
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class User(models.Model):
    image = models.ImageField(blank=True, null=True)
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.django_user.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class QuestionManager(models.Manager):
    def get_latest(self):
        # return self.all().order_by('-created')    # сложна сюда впилить join и sum!
        return self.raw("""
        SELECT 
                sum(lq.mark) AS likes_cnt, 
                * 
        FROM app_question q
            LEFT JOIN app_likequestions lq 
                ON q.id = lq.question_id 
        GROUP BY lq.question_id 
        ORDER BY q.created DESC;
        """)

    def get_hottest(self):
        return self.raw("""
        SELECT 
                sum(lq.mark) AS likes_cnt, 
                * 
        FROM app_question q
            LEFT JOIN app_likequestions lq 
                ON q.id = lq.question_id 
        GROUP BY lq.question_id 
        ORDER BY likes_cnt DESC;
        """)

    def get_by_tag(self, tag_text):
        # return self.filter(tag__text=tag_text)    # сложна сюда впилить все joinы и sum!
        return self.raw("""
        SELECT
                sum(lq.mark) AS likes_cnt,
                *
        FROM app_question q
            INNER JOIN app_question_tag qt
                ON (q.id = qt.question_id)
            INNER JOIN app_tag t
                ON (qt.tag_id = t.id AND t.text = 'behavior')
            LEFT JOIN app_likequestions lq
                ON q.id = lq.question_id
        GROUP BY lq.question_id
        ORDER BY q.created DESC;
        """)


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def get_by_question(self, question_id):
        return self.filter(question_id=question_id).order_by('-id')


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
    mark = models.IntegerField(default=1)

    class Meta:
        unique_together = ['question', 'user']
