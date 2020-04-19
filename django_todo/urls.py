"""django_todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from todo_app.views import *
from todo_app.sitemap import BlogSitemap 
from todo_app import urls as api_urls


admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'ООО КРАССУЛА'
admin.site.index_title = 'Панель администратора'

sitemaps = [BlogSitemap]

urlpatterns = [
	url(r'^admin/preferences/$', admin_views),
    url(r'^admin/analyze/$', analyze_views),
    url(r'^admin/', admin.site.urls),
    url(r'^contacts', contacts_views),
    url(r'^search', search_views),
    url(r'^about', about_views),
    url(r'^news', news_views),
    url(r'^catalog', catalog_views),
    url(r'^akcii', akcii_views),
    url(r'^new_product', new_product_view),
    url('^prod/(?P<prod_id>.+)/$', TovarsApiView.as_view()),
    url(r'^orders/(?P<name_user>[\w-]+)/(?P<mail_user>[\w-]+)/(?P<prod_id>.+)$', orders_add),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': {'blog':BlogSitemap,}}),
    url(r'^robots.txt', TemplateView.as_view(template_name="todo_app/robots.txt", content_type='text/plain')),
     url(r'^app', TemplateView.as_view(template_name="todo_app/mobile_app.apk")),
    url(r'^$', main_views),
    url(r'^main2', main_views2),
    url(r'^mobileab', about_views2),
    url(r'^prazdnik', prazdnik_view),
    url(r'^mobileca', catalog_views2),
    url(r'^mobileco', contacts_views2),
    url(r'^catmobile/category/(?P<category_slug>[\w-]+)/$', list_product_view2, name='category_detail'),
    url(r'^category/(?P<category_slug>[\w-]+)/$', list_product_view, name='category_detail'),
    url(r'^product/(?P<product_slug>[\w-]+)/$', product_view, name='product_detail'),
    url(r'^mobileprod/product/(?P<product_slug>[\w-]+)/$', product_view2, name='product_detail'),
    url(r'^api/', include(api_urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
