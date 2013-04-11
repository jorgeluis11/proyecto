# Create your views here.
from django.views.generic import DetailView
from .models import Article, Category, Type, ArticleComment
from django.shortcuts import render, HttpResponseRedirect, render_to_response
from articles.forms import NewsForm, QuoteForm, MovieForm, ComentaryForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.http import HttpResponse

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
    if request.POST:
        form = NewsForm(request.POST)
        print "error", form['categoria'].errors
        if form.is_valid:
            title = form.cleaned_data['titulo']
            content = form.cleaned_data['contenido']
            category = form.cleaned_data['categoria']
            # photo = request.FILES['foto']
            type = Type.objects.get(name="Noticias")
            category = Category.objects.get(name=category)

            Article(user_id=request.user, type=type, category=category,
                    title=title, content=content).save()

    news_form = NewsForm()
    quotes_form = QuoteForm()
    movies_form = MovieForm()

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
        if q is not None and q:
            data = {
            "noticias": Article.objects.filter(type__name="Noticias", title__startswith=q).order_by('-submit_date')[:3]
            }
            return render(request,"articles/search.html", data)
        else:

            data = {
            "tips": Article.objects.all().order_by('?')[:4]
            }
            return render_to_response("articles/searchFail.html", data)