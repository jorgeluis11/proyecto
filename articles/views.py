# Create your views here.
from django.views.generic import DetailView
from .models import Article, Category, Type
from django.shortcuts import render
from articles.forms import NewsForm

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'noticias/index.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().exclude(name="None").order_by("name")
        return context

    #     # professor = self.object
    #     # if self.request.GET:
    #     #     page = self.request.GET['page']
    #     # else:
    #     #     page = 1
    #     # context['page'] = professor.generate_comments(page)

    #     # university = University.objects.get(
    #     #     notaso_id=professor.notaso_university_id)

    #     # context['university'] = university.percent()

    #     # context['department'] = Professor.objects.department_percent(
    #     #     professor.department)
    #     return context


def create(request):
    if request.POST:
        form = NewsForm(request.POST)
        if form.is_valid:
            # category = form.cleaned_data['categoria']
            # print "Category", category
            title = form.cleaned_data['titulo']
            print "Title", title
            content = request.POST['contenido']
            article = Article(type=Type(name="Noticias"), category=Category(name=category))
    else:
        news_form = NewsForm()

    data ={
    "news_form":news_form,
    }
    return render(request,"articles/create.html", data)

def add_article(request):

    return render(request,"")
