from django.contrib.sitemaps import Sitemap
from .models import Products

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Products.objects.all()