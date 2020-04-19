from todo_app.models import *
import xlrd
import os.path
from xlutils.copy import copy
import xlwt

def update_price(file, form_elem):
	file = Prais.objects.all().last().upload
	wb = xlwt.Workbook(file)
	ws = wb.add_sheet('Sheet1') 
	ws.write(9, 0, 11)
	ws.write(9, 1, 'iii')
	ws.write(9, 2, 387653)
	test=wb.save(form_elem)
	price = Prais(upload=rb.save(test))
	price.save()