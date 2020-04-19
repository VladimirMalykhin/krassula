# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator
from todo_app.models import *
import csv
import os
from .excel import *
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
from .forms import *
from .check import *
import math 
import xlrd
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def contacts_views(request):
    return render(request, 'todo_app/contacts.html', {
    })


def catalog_views(request):
    categories_list = Categories.objects.filter()
    categories_count = categories_list.count()
    pagination_page = int(math.ceil(categories_count / 15 ))
    paginator = Paginator(categories_list, 15)
    if(request.GET.get('page')):
        page = request.GET.get('page')
        try:
            int(page)
        except ValueError:
            page = 1
        if(int(page) > pagination_page):
            page = 1
    else:
        page = 1
    categories = paginator.page(page)
    return render(request, 'todo_app/catalog.html', {
       'categories':categories,
    })

def check_admin(user):
   return user.is_staff
   
@user_passes_test(check_admin)
def admin_views(request):
	form = PraisForm()
	if request.method == 'POST':
		form = PraisForm(request.POST, request.FILES)
        
		if(form.is_valid()):
			Products.objects.all().update(is_stock=False)
			Filter.objects.all().delete()
			test = form.cleaned_data['upload']
			one = Prais(upload=test)
			one.save()
			file = Prais.objects.all().last().upload
			wb = xlrd.open_workbook(file_contents=file.read()) 
			sheet = wb.sheet_by_index(0)
			for i in range(5, sheet.nrows):
				try:
					title = sheet.cell_value(i, 0)
					type = sheet.cell_value(i, 1)
					descr = sheet.cell_value(i, 2)
					price = int(sheet.cell_value(i, 3))
					url = sheet.cell_value(i, 4)
					category_excel = sheet.cell_value(i, 5)
					manufacturer_excel = sheet.cell_value(i, 6)
					measure_excel = sheet.cell_value(i, 7)
				except Exception as e:
					error_message = 'Неправильная структура документа'
					return render(request, 'admin/preferences.html', {
       	'form' : form, 
        'error': sheet.cell_value(i, 9),
	})
				try:
					manufacturer = Manufacturer.objects.get(name=manufacturer_excel)
				except Exception as e:
					error_message = 'Производитель' + manufacturer_excel + 'не найден'
					return render(request, 'admin/preferences.html', {
       	'form' : form, 
        'error': error_message,
	})
				try:
					measure = Measurements.objects.get(name=measure_excel)
				except Exception as e:
					error_message = 'Единица измерения' + measure_excel + 'не найдена'
					return render(request, 'admin/preferences.html', {
       	'form' : form, 
        'error': error_message,
	})
				try:
					category = Categories.objects.get(name=category_excel)
				except Exception as e:
					error_message = 'Категория' + category_excel + 'не найдена'
					return render(request, 'admin/preferences.html', {
       	'form' : form, 
        'error': error_message,
	})
				product = Products.objects.filter(slug=url).count()
				if(product>0):
					Products.objects.filter(slug=url).update(is_stock=True, name=title, type_product=type, price=price, short_description=descr, manufacturers=manufacturer, measure=measure)
				else:
					similar_product = Products.objects.filter( name=title,type_product=type,short_description=descr, measure=measure).count()
					if(similar_product>0):     
						Products.objects.filter( name=title,type_product=type,short_description=descr).update(is_manufacturer_filter=True)
						current_product = Products.objects.get( name=title,type_product=type,short_description=descr)
						filter = Filter(product=current_product, manufacturer=manufacturer, price=price)
						filter.save()
					else:
						product_title = Products.objects.filter(name=title).count()
						if(product_title>0):
							product_photo1 = Products.objects.filter(name=title)[0].photo
							product_photo2 = Products.objects.filter(name=title)[0].big_photo
							child_category = Products.objects.filter(name=title)[0].child_category
						else:
							product_photo1="/media/images/test.jpg"
							product_photo2="/media/images/test.jpg"
							child_category = Child_Categories.objects.get(name='Test')
						new_product = Products(name=title, type_product=type, photo=product_photo1, big_photo = product_photo2, short_description = descr, text_description = title, title=title, keywords = title, tag_description= title, is_manufacturer_filter=False, is_stock=True, category=category, price=price, slug=url, manufacturers=manufacturer, measure=measure, child_category=child_category)
						new_product.save()
			Prais.objects.all().delete()
			update_price(wb)
			return render(request, 'admin/preferences.html', {
       	'form' : form, 
        'error': 'Товары успешно загружены',
	})
	return render(request, 'admin/preferences.html', {
        'form' : form,    
	})
	
    
def about_views(request):
    return render(request, 'todo_app/about.html', {
    })


def news_views(request):
    news = News.objects.all()
    return render(request, 'todo_app/news.html', {
        'news':news,
    })


def akcii_views(request):
    return render(request, 'todo_app/akcii.html', {
    })


def main_views(request):
    return render(request, 'todo_app/index.html', {
    })


def list_product_view(request, category_slug):
    category = Categories.objects.get(slug=category_slug)
    child_categories = Child_Categories.objects.filter(base_category=category)    	
    products_list = Products.objects.filter(category=category_slug)
    products_count = products_list.count()
    all_products = Products.objects.all()
    pagination_page = int(math.ceil(products_count / 15 ))
    paginator = Paginator(products_list, 15)
    if(request.GET.get('page')):
        page = request.GET.get('page')
        try:
            int(page)
        except ValueError:
            page = 1
        if(int(page) > pagination_page):
            page = 1
    else:
        page = 1
        products = paginator.page(page)
    return render(request, 'todo_app/products.html', {
            'category_name':category.name,
            'products':products_list,
            'all_products':products,
            'child_categories':child_categories
        })
    
def list_product_view2(request, category_slug):
    category = Categories.objects.get(slug=category_slug)    	
    products_list = Products.objects.filter(category=category_slug)
    return render(request, 'todo_app/products2.html', {
            'category_name':category.name,
            'products':products_list,
        })


def product_view(request, product_slug):
    
    product = Products.objects.get(slug=product_slug)
    error =""
    form = OrderForm()
    category_slug = product.category
    category = Categories.objects.get(name=category_slug)
    if (product.is_manufacturer_filter is True):
        manufactures = Filter.objects.filter(product=product).order_by('price')
    else:
        manufactures = ""
    products_list = Products.objects.filter(category=category_slug)[:3]
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if(form.is_valid()):
            check_object = FormChecking()
            name_user = form.cleaned_data['name_user']
            mail_user = form.cleaned_data['mail_user']
            result_name = check_object.check('name', name_user)
            result_mail = check_object.check('mail', mail_user)
            quantity = form.cleaned_data['quantity']
            manufacturer = form.cleaned_data['manufacturer']
            product_id = product
            price = product.price
            if(result_name == 'Ok' and result_mail == 'Ok'):
                order = Orders(name_user=name_user, mail_user=mail_user, quantity=quantity, product_id=product_id, price=price, manufacturer=manufacturer)
                order.save()
                error = 1
            else:
                error = 2
    return render(request, 'todo_app/carta_tovara.html', {
        'product': product,
        'categories' : category,
        'category_id':category_slug,
        'products':products_list,
        'form': form,
        'manufactures': manufactures,
        'error':error
    })
