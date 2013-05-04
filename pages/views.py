from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import login, authenticate, logout
from profiles.models import NotasoUser
from articles.models import Article, Category
from random import shuffle
from werkzeug.wrappers import Request, Response

#Use Wekzeug debugging for django
@Request.application
def application(request):
    return Response('Hello World!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)

"""
Get the top, recent_quotes, recent_news 
And send the data to the template.
"""
def home(request):
    popular_articles = Article.objects.top(limit=5,type="Noticias") + Article.objects.top(limit=5, type="Movies") + list(Article.objects.filter(type__name="Quotes")[:5])
    popular_articles.sort(key=lambda x: x.percent(), reverse=True)
    recent_quotes = Article.objects.filter(type__name="Quotes").order_by('-submit_date')[:3]
    recent_news = Article.objects.filter(type__name="Noticias").order_by('-submit_date')[:4]
    recent_movies = Article.objects.filter(type__name="Movies").order_by('-submit_date')[:8]

    data = {
        'popular_articles' : popular_articles,
        'recent_quotes'    : recent_quotes,
        'recent_news'      : recent_news,
        'recent_movies'    : recent_movies
    }
    return render(request, 'pages/home.html', data)

"""
Get the top_news, every category, one radom news of each category 
And send all the data to the template.
"""
def noticias(request):
    top_news = Article.objects.top(limit=15, type="Noticias")
    categories = Category.objects.all().exclude(name="None").order_by("name")
    recent_news = []
    try:
        recent_news.append(Article.objects.filter(category__name="Deportes").order_by('?')[0])
    except:
        print "Error!"
    try:
        recent_news.append(Article.objects.filter(category__name="Economia").order_by('?')[0])
    except:
        print "Error!"
    try:
        recent_news.append(Article.objects.filter(category__name="Entretenimiento").order_by('?')[0])
        recent_news.append(Article.objects.filter(category__name="Internacionales").order_by('?')[0])
        recent_news.append(Article.objects.filter(category__name="Local").order_by('?')[0])
        recent_news.append(Article.objects.filter(category__name="Politica").order_by('?')[0])
        recent_news.append(Article.objects.filter(category__name="Tecnologia").order_by('?')[0])
        recent_news.append(Article.objects.filter(category__name="Vida").order_by('?')[0])
    except:
        print"Error!"

    data={
        'top_news': top_news,
        'recent_news': recent_news,
        'categories': categories,

    }
    return render(request, 'pages/noticias.html', data)

"""
If the user is not log in and doesn't exist in the database 
store all the information to the UserProfile but if it exist 
on the data base only log in the user.
"""
def register_login(request):
    print request.POST
    if not request.user.is_authenticated():
        if request.method == "POST":
            try:
                user = NotasoUser.objects.get(facebook_id=request.POST['id'])
            except Exception:
                print "USEr vacio"
                print request.POST['email']
                # user = NotasoUser.objects.all()[0]
                user = NotasoUser(email=request.POST['email'])
                user.set_password(None)
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


"""
This function log out the user
And send all the data to the template.
"""
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
