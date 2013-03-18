from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import login, authenticate, logout
from profiles.models import NotasoUser
from articles.models import Article, Category
import random
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    return Response('Hello World!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)


def home(request):
    # popular_articles = sorted(Article.objects.top(), key=lambda x: random.random())[:15]
    popular_articles = Article.objects.top(limit=15)
    recent_quotes = Article.objects.filter(type__name="Quotes").order_by('-submit_date')[:3]
    recent_news = Article.objects.filter(type__name="Noticias").order_by('-submit_date')[:4]
    colors = ["#21BB21"]

    for article in recent_news:
        article.color = colors[random.randrange(0, len(colors))]

    data = {
        'popular_articles': popular_articles,
        'recent_quotes': recent_quotes,
        'recent_news': recent_news,
    }
    return render(request, 'pages/home.html', data)


def noticias(request):
    top_news = Article.objects.top(type="Noticias")[:5]
    categories = Category.objects.all().exclude(name="None").order_by("name")
    recent_news = []
    recent_news.append(Article.objects.filter(category__name="Local").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Deportes").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])
    recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])

    data = {
        'top_news': top_news,
        'recent_news': recent_news,
        'categories': categories,

    }
    return render(request, 'noticias/noticias.html', data)


def register_login(request):
    print request.POST['first_name']
    if not request.user.is_authenticated():
        if request.method == "POST":
            try:
                user = NotasoUser.objects.get(facebook_id=request.POST['id'])
            except Exception:
                print "USEr vacio"
                print request.POST['email']
                user = NotasoUser.objects.create_user(email=request.POST['email'])
                print "entro"  
                user.facebook_name = request.POST['name']
                user.facebook_id = request.POST['id']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.gender = request.POST['gender']
                user.save()
            user = authenticate(username=user.email)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print "log in Sucess!"
    return HttpResponseRedirect('/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
