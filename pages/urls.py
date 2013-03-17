from django.conf.urls import patterns, url
from articles.views import NewsDetailView, create

urlpatterns = patterns('pages.views',
    url(r'^$', 'home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^noticias/', 'noticias',
    url(
        regex=r'^noticias/(?P<pk>\d+)',
        view=NewsDetailView.as_view(),
        name='News'
        ),
    url(r'^create/', create),
)