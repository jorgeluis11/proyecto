# Create your views here.
from django.views.generic import DetailView
from .models import Article, Category, Type
from django.shortcuts import render
from articles.forms import NewsForm, QuoteForm, MovieForm

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
    return render(request,"articles/create.html", data)

def add_article(request):

    return render(request,"")
