from django.conf.urls import patterns, include, url
from django.conf import settings
from pages.views import register_login, logout_user, noticias
from articles.views import ArticleDetailView, create
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pages.views.home', name='home'),
    url(r'^register_login$', register_login ,name='user_validation' ),
    url(r'^logout$', logout_user ,name='logout' ),
    
    url(
        regex=r'^noticias/(?P<pk>\d+)',
        view=ArticleDetailView.as_view(),
        name='article',
    ),

    url(r'^noticias/', noticias, name="noticias") ,
    
    url(r'^create/', create),

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

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATICFILES_DIRS[0], 'show_indexes': True}),
    )