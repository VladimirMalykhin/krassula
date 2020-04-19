# -*- coding: utf-8 -*-
import re

class FormChecking(object):
    Values = {
'name': {'min':3, 'max': 25, 'type': "string", 'is_mail':False},
'mail': {'max': 30, 'min': 3, 'type':"string", 'is_mail':True},
'phone': {'min': 7, 'max': 15, type:"integer", 'is_mail':False},
	}
    
    def check(self, field, value):
        html_tags = re.compile('<.*?>')
        text_value = re.sub(html_tags, '', value)
        min_length = self.Values[field]['min']
        is_mail = self.Values[field]['is_mail']
        max_length = self.Values[field]['max']
        type = self.Values[field]['type']
        if(len(text_value) < min_length):
            return 'Введите значение'
        elif(len(text_value) > max_length):
            return 'Превышено максимальное хначение'
        if(is_mail is True):
            if('@' in text_value):
                pass
            else:
                return 'Отсутствует @'
        return 'Ok'