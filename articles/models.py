from django.db import models
from profiles.models import NotasoUser
from django.contrib.comments.models import Comment
import datetime


class ArticleManager(models.Manager):

    def top(self, type="all", category="all", limit=5):
        return self.__edges('top', type, category, limit)

    def worst(self, type="all", category="all", limit=5):
        return self.__edges('worst', type, category, limit)

    def __edges(self, edge, type, category, limit):
        if edge == "top":
            order = "-"
        else:
            order = ""

        if type == "all" and category == "all":
            print "all"
            return Article.objects.all().order_by(order+"user_count")[:limit]
        else:
            print "%suser_count" % order
            return Article.objects.filter(type__name=type).order_by(order+"user_count")[:limit]


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name



def get_url(instance, filename):
    return 'img/%s' % filename


class Article(models.Model):
    user_id = models.ForeignKey(NotasoUser)
    type = models.ForeignKey(Type)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=2500)
    photo = models.ImageField(upload_to=get_url, blank=True)
    submit_date = models.DateField(default=datetime.datetime.now())
    user_count = models.IntegerField()
    user_rating = models.IntegerField()
    objects = ArticleManager()

    def percent(self):
        return (float(self.user_rating) / self.user_count) * 20

    def __unicode__(self):
        return self.title


class ArticleCommentManager(models.Manager):

    def __edges(self, edge, limit):
        return "algo"


class ArticleComment(Comment):
    Article_id = models.ForeignKey(Article)
    objects = ArticleCommentManager()

    def __unicode__(self):
        return self.name
