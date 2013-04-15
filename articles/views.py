# Create your views here.
from django.views.generic import DetailView
from .models import Article, Category, Type, ArticleComment, ArticleRating
from django.shortcuts import render, HttpResponseRedirect, render_to_response
from articles.forms import NewsForm, QuoteForm, MovieForm, ComentaryForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.http import HttpResponse
from profiles.models import NotasoUser
from django.utils import timezone
import json

"""
Class based view to show the article and 
extra data to show the category
Send the data to the template.
"""
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'noticias/index.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().exclude(name="None").order_by("name")
        context['comentaryform'] = ComentaryForm()
        try:
            context['rating'] = ArticleRating.objects.get(Article_id=self.object.pk,
                                                      user_id=self.request.user.pk)
        except Exception, e:
            print "No le ha dado puntuacion"
        
        ct = ContentType.objects.get_for_model(ArticleComment)
        context['comments'] = ArticleComment.objects.filter(content_type=ct,
            object_pk=self.object.pk)
        return context

"""
Class based view to show the the category section and 
extra data to show the category
Send the data to the template.
"""
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'articles/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().exclude(name="None").order_by("name")
        return context


"""
Function based view to show the article and 
This function create an article and store it in the database
and send all the forms to the template.
"""

def create(request):
    news_form = NewsForm()
    quotes_form = QuoteForm()
    movies_form = MovieForm()
    if request.GET:
        if request.POST:
            if request.GET["type"] == "news":
                news_form = NewsForm(request.POST, request.FILES)
                if news_form.is_valid():
                    title = news_form.cleaned_data['titulo']
                    content = news_form.cleaned_data['contenido']
                    category = news_form.cleaned_data['categoria']
                    photo = news_form.cleaned_data['foto']
                    type = Type.objects.get(name="Noticias")
                    category = Category.objects.get(name=category)
                    print timezone.now()
                    Article(user_id=request.user, type=type, category=category,
                            title=title, content=content, photo=photo, submit_date=timezone.now()).save()
            elif request.GET["type"] == "quotes":
                quotes_form = QuoteForm(request.POST)
                if quotes_form.is_valid():
                    autor = quotes_form.cleaned_data['autor']
                    frase = quotes_form.cleaned_data['frase']
                    type = Type.objects.get(name="Quotes")
                    category = Category.objects.get(name="None")
                    Article(user_id=request.user, category=category, type=type,
                            title=autor, content=frase).save()  
            elif request.GET["type"] == "movies":
                movies_form = MovieForm(request.POST)
                if quotes_form.is_valid():
                    autor = movies_form.cleaned_data['autor']
                    frase = movies_form.cleaned_data['review']
                    type = Type.objects.get(name="Movies")
                    category = Category.objects.get(name="None")
                    Article(user_id=request.user, category=category, type=type,
                            title=autor, content=frase).save()  
                return HttpResponseRedirect("/")  
    data = {
        "news_form": news_form,
        "quotes_form": quotes_form,
        "movies_form": movies_form,
    }
    return render(request, "articles/create.html", data)


def add_comment(request, pk):
    if request.method == "POST":
        form = ComentaryForm(request.POST)
        if form.is_valid:
            comment = request.POST['comment']
            ct = ContentType.objects.get_for_model(ArticleComment)
            ArticleComment(content_type=ct, object_pk=pk, 
                           user=request.user, site=Site.objects.get(id=1), 
                           comment=comment, Article_id=Article.objects.get(id=1)).save()
    return HttpResponseRedirect("/article/"+pk)

def search(request):
    data = {}
    if request.is_ajax():
        q = request.GET.get('q')
        if q[0] == "@":
            q = q[1:len(q)]
            try:
                usuario = NotasoUser.objects.get(facebook_name__contains=q)
                data = {
                    'usuario': usuario,
                    'articles': usuario.article_set.all().order_by("?")[:5]
                }
                return render(request,"articles/search.html", data)
            except:
                data = {
                    'users': NotasoUser.objects.all().order_by("?")[:5]
                }
                return render(request,"articles/searchFail.html", data)
        else:
            if q is not None and q:
                data = {
                "articles": Article.objects.filter(title__startswith=q).order_by('-submit_date')
                }
                if data["articles"]:
                    return render(request,"articles/search.html", data)
                data = {
                "articles": Article.objects.all().order_by('?')[:5]
                }
    return render(request,"articles/searchFail.html", data)

def autocomplete(request):
    if request.is_ajax():
        result = []
        q = request.GET.get('q')
        if q is not None:
            if q[0] == "@":
                print "AAAAaaaaa"
                q = q[1:len(q)]
                users = NotasoUser.objects.filter(facebook_name__startswith=q).order_by("?")[:8]
                for user in users:
                    result.append("@"+ user.facebook_name)
                print result
                return HttpResponse(json.dumps(result), mimetype="application/json")
            if q:
                articles = Article.objects.filter(type__name="Noticias", title__startswith=q).order_by('-submit_date')[:8]
                for article in articles:
                    result.append(article.title[:25])
            return HttpResponse(json.dumps(result), mimetype="application/json")
    return HttpResponseRedirect('/home')
    
def javascript_filter(request):
    return render_to_response("articles/filterContent.html",{"content":request.GET.get('content')})


def rating(request):
    if request.is_ajax():
        if request.POST:
            user = NotasoUser.objects.get(pk=request.POST['user'])
            article = Article.objects.get(pk=request.POST['article'])
            rating = request.POST['rating']
            ArticleRating(user_id=user, Article_id=article, rate=rating).save()
    return HttpResponse("Rated")