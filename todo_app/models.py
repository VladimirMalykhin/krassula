# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.core.urlresolvers import reverse
from todo_app.choices import *
from django.db import models
from django.utils.html import format_html

# Create your models here.
	
class Search(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

class Analyz(models.Model):
	name = models.CharField(max_length=255, verbose_name="Название")
    
class Question(models.Model):
    mail_user = models.CharField(max_length=255, verbose_name="Почта")
    name_user = models.CharField(max_length=255, verbose_name="Имя")
    text = models.TextField(verbose_name="Вопрос")
    
class Compare(models.Model):
	our_product = models.URLField(max_length=200)
	concurent_product = models.URLField(max_length=200)
    
    
class Category_Analyze(models.Model):
	url = models.URLField(max_length=200)
    
class Site_Analyze(models.Model):
	url_site = models.URLField(max_length=200)
    
class Site_Feedbacks(models.Model):
	user = models.CharField(max_length=255, verbose_name="Пользователь")
	text = models.TextField(verbose_name="Отзыв")
	raiting = models.IntegerField(choices=FEEDBACKS, default=1, verbose_name="Статус")


class Site_Feedback(models.Model):
	user = models.CharField(max_length=255, verbose_name="Пользователь")
	text = models.TextField(verbose_name="Отзыв")
	raiting = models.IntegerField(choices=FEEDBACKS, default=1, verbose_name="Статус")
	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы о сайте'
        

class Categories(models.Model):
	name = models.CharField(max_length=50, unique=True, verbose_name="Название")
	photo = models.ImageField(upload_to='images/', verbose_name="Фото")
	description = models.TextField(verbose_name="Описание", default='' )
	slug = models.SlugField(blank=True, unique=True, verbose_name="URL")
	def __str__(self):
	    return self.name

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'category_slug': self.slug})
    
    
	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

class Prais(models.Model):
	upload = models.FileField(upload_to='media/')
	created_at = models.DateTimeField(auto_now_add=True)
    
	class Meta:
		verbose_name = 'Прайс'
		verbose_name_plural = 'Прайс-листы'
        
class Manufacturer(models.Model):
	name = models.CharField(max_length=50,verbose_name="Название" )
	country = models.CharField(max_length=50, verbose_name="Страна" )

	def __str__(self):
	    return self.name
    
	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'

class Child_Categories(models.Model):
	name = models.CharField(max_length=50,verbose_name="Название" )
	base_category = models.ForeignKey(Categories,related_name='base',verbose_name="Категория")
	tag_id = models.CharField(max_length=50,verbose_name="Id", default="home")
	def __str__(self):
	    return self.name + ' (' + self.base_category.name + ')'
    
	class Meta:
		verbose_name = 'Подкатегория'
		verbose_name_plural = 'Подкатегории'


class Measurements(models.Model):
	name=models.CharField(max_length=50,verbose_name="Название" )
	def __str__(self):
		return self.name
    
	class Meta:
		verbose_name = 'Единица'
		verbose_name_plural = 'Единицы измерения'
        
        
class Products(models.Model):
	name = models.CharField(max_length=50, verbose_name="Название" )
	type_product = models.CharField(max_length=50, verbose_name="Вид" )
	short_description = models.CharField(max_length=255, verbose_name="Краткое описание" )
	text_description = models.TextField(verbose_name="Полное описание" )
	title = models.CharField(max_length=100)
	keywords = models.CharField(max_length=100)
	tag_description = models.CharField(max_length=200)
	is_manufacturer_filter = models.BooleanField(default=True, verbose_name="Наличие фильтра" )
	is_stock = models.BooleanField(default=True, verbose_name="В наличии")
	manufacturers = models.ForeignKey(Manufacturer, related_name="manu",blank=True,verbose_name="Производитель" )
	price = models.DecimalField(verbose_name="Цена",max_digits=7, decimal_places=2)
	category = models.ForeignKey(Categories, to_field="slug", related_name='variations',verbose_name="Категория" )
	measure = models.ForeignKey(Measurements, related_name="measu",blank=True,verbose_name="Единица измерения", default=0 )
	child_category = models.ForeignKey(Child_Categories, related_name="child",blank=True, default=0, verbose_name="Подкатегория" )
	slug = models.SlugField(blank=True, unique=True,verbose_name="URL" )
	photo = models.CharField(max_length=150, verbose_name="Фото в каталоге" )
	big_photo = models.CharField(max_length=150, verbose_name="Фото в карточке" )
	price_sale = models.DecimalField(verbose_name="Цена по акции", max_digits=7, decimal_places=2)
	def __str__(self):
	    return self.name + '  '+self.slug

	def get_absolute_url(self):
		return reverse('product_detail', kwargs={'product_slug': self.slug})
    
	def as_dict(self): 
		return { 
			"id": self.id, 
			# other stuff 
		}
    
    
	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'


class Orders(models.Model):
	name_user = models.CharField(max_length=50, default="",verbose_name="Имя заказчика" )
	mail_user = models.CharField(max_length=100, default="",verbose_name="Почта заказчика" )
	product_id = models.ForeignKey(Products, related_name='variations',verbose_name="Продукт" )
	quantity = models.IntegerField(verbose_name="Количество", default=1 )
	price = models.DecimalField(max_length=50, max_digits=10, decimal_places=2,verbose_name="Цена" )
	manufacturer = models.CharField(max_length=50,verbose_name="Производитель" )
	def __str__(self):
	    return self.name_user
    
	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

class Products_Feedback(models.Model):
	user = models.CharField(max_length=255, verbose_name="Пользователь")
	text = models.TextField(verbose_name="Отзыв")
	raiting = models.IntegerField(choices=FEEDBACKS, default=1, verbose_name="Статус")
	product = models.ForeignKey(Products, related_name='variations2',verbose_name="Продукт" )
	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы о товарах'
        
        
class News(models.Model):
	name = models.CharField(max_length=50,verbose_name="Название" )
	photo = models.ImageField(upload_to='images/',verbose_name="Фото" )
	short_description = models.CharField(max_length=255,verbose_name="Краткое описание" )
	description = models.TextField(verbose_name="Полное описание" )
	

	def __str__(self):
	    return self.name.encode('utf-8')
    
	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'

    
class Filter(models.Model):
	product = models.ForeignKey(Products, related_name='products',verbose_name="Продукт" )
	manufacturer = models.ForeignKey(Manufacturer, related_name='filters',verbose_name="Производитель" )
	price = models.DecimalField(verbose_name="Цена",max_digits=7, decimal_places=2)
	def __str__(self):
	    return self.product.name
        
	class Meta:
		verbose_name = 'Фильтр'
		verbose_name_plural = 'Фильтры'
