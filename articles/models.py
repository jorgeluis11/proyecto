from django.db import models
from profiles.models import NotasoUser
from django.contrib.comments.models import Comment
from django.utils import timezone
import operator
from django.db.models import Max


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
            return sorted( Article.objects.all(type__name=type), key=lambda x: x.percent(), reverse=True)[:limit]
        elif (type == "Noticias" or type == "Quotes" or type == "Movies") and category == "all":
            print "ALLL!!"
            return sorted( Article.objects.filter(type__name=type), key=lambda x: x.percent(), reverse=True)[:limit]
        else:
            print "Category!!"
            return sorted( Article.objects.filter(type__name=type, category__name=category), key=lambda x: x.percent(), reverse=True)[:limit]

class Category(models.Model):
    categories = (
        ("None", "None"),
        ("Deportes", "Deporte"),
        ("Economia", "Economia"),
        ("Entretenimiento", "Entretenimiento"),
        ("Internacionales", "Internacional"),
        ("Local", "Local"),
        ("Politica", "Politica"),
        ("Tecnologia", "Tecnologia"),
        ("Vida", "Vida"),
    )
    name = models.TextField(max_length=60, choices=categories)

    def __unicode__(self):
        return self.name


class Type(models.Model):
    types = (("Noticias", "Noticias"),
        ("Quotes", "Quotes"),
        ("Movies", "Movies"),
    )
    name = models.TextField(max_length=60, choices=types)

    def __unicode__(self):
        return self.name

def get_url(instance, filename):
    return 'img/%s' % filename


class Article(models.Model):
    user_id = models.ForeignKey(NotasoUser)
    type = models.ForeignKey(Type)
    category = models.ForeignKey(Category)
    title = models.TextField(max_length=80)
    content = models.TextField(max_length=2500)
    photo = models.ImageField(upload_to=get_url, blank=True)
    submit_date = models.DateTimeField(('date/time submitted'), default=timezone.now())
    user_count = models.IntegerField(default=0)
    user_rating = models.IntegerField(default=0)
    objects = ArticleManager()

    def rating(self):
        _rate = self.articlerating_set.all()
        if len(_rate) == 0:
            return 0
        else: 
            rate = 0
            for x in _rate:
                rate += x.rate
            return round(float(rate)/len(_rate))

    def user_counting(self):
        _rate = self.articlerating_set.all()
        if len(_rate) == 0:
            return "Puntuacion: 0" 
        rate = 0
        for x in _rate:
            rate += x.rate
        return str(round(float(rate)/len(_rate),1)) + " de " + str(len(_rate)) + " usuarios"
    
    def percent(self):
        _rate = self.articlerating_set.all()
        if len(_rate) == 0:
            return 0
        else:
            rate = 0
            for x in _rate:
                rate += x.rate
            return round(float(rate)/len(_rate),5)

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


class ArticleRating(models.Manager):

    def __edges(self, edge, limit):
        return "algo"

class ArticleRating(models.Model):
    rate = models.IntegerField()
    user_id = models.ForeignKey(NotasoUser)
    Article_id = models.ForeignKey(Article)
    objects = ArticleRating()

    def __unicode__(self):
        return str(self.rate)