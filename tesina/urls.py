from django.conf.urls import patterns, include, url
from django.conf import settings
from pages.views import register, logout_user, noticias
from articles.views import ArticleDetailView, create, remove, CategoryDetailView, add_comment, search, autocomplete, javascript_filter, rating, quotes, movies
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# URLS of the proyect, the Django urls use regular 
# expressions to find the view methods 

urlpatterns = patterns('',
    url(r'^$', 'pages.views.home', name='home'),
    url(r'^register$', register ,name='user_validation' ),
    url(r'^logout$', logout_user ,name='logout' ),

    url(r'^quotes/', quotes, name="quotes"),
    url(r'^movies/', movies, name="movies"),
    
    url(
        regex=r'^article/(?P<pk>\d+)',
        view=ArticleDetailView.as_view(),
        name='article',
    ),

    url(r'^noticias/', noticias, name="noticias") ,

    url(
        regex=r'^article/(?P<pk>\d+)',
        view=ArticleDetailView.as_view(),
        name='article',
    ),
    
    url(
        regex=r'^category/(?P<pk>\d+)',
        view=CategoryDetailView.as_view(),
        name='category',
    ),

    url(r'^addcomment/(?P<pk>\d+)', add_comment),

    url(r'^create/', create),
    url(r'^remove/', remove),
    url(r'^autocomplete/', autocomplete),
    url(r'^search/', search, name="search"),
    url(r'^jsfilter/', javascript_filter),
    url(r'^rating/', rating),

    # Examples:
    # url(r'^$', 'portfolio.views.home', name='home'),
    # url(r'^portfolio/', include('portfolio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATICFILES_DIRS[0], 'show_indexes': True}),
)