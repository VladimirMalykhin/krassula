# -*- coding: utf-8 -*-
from django import forms
from todo_app.models import *

class PraisForm(forms.ModelForm):
	class Meta:
		model = Prais
		exclude = ['created_at']
        

class SearchForm(forms.ModelForm):
	class Meta:
		model = Search
		exclude = []

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = []
        
        
class FeedBackSiteForm(forms.ModelForm):
	class Meta:
		model = Site_Feedback
		exclude = []
		widgets = {'raiting': forms.HiddenInput(),

		}


class FeedBackProductsForm(forms.ModelForm):
	class Meta:
		model = Products_Feedback
		exclude = ['product']
		widgets = {'raiting': forms.HiddenInput(),
        
		}


class CompareForm(forms.ModelForm):
	class Meta:
		model = Compare
		exclude = []
        
class SiteAnalyzeForm(forms.ModelForm):
	class Meta:
		model = Site_Analyze
		exclude = []
        
        
class CategoryAnalyzeForm(forms.ModelForm):
	class Meta:
		model = Category_Analyze
		exclude = []
        
        
class OrderForm(forms.ModelForm):
	class Meta:
		model = Orders
		exclude = ["product_id","price"]
		widgets = {'quantity': forms.HiddenInput(),
		'manufacturer': forms.HiddenInput(),
		'name_user' : forms.TextInput(attrs={'class': 'form-control'}),
		'mail_user' : forms.TextInput(attrs={'class': 'form-control'}),

		}
		labels = {
            'name_user': ('Имя'),
            'mail_user': ('Почта'),
        }