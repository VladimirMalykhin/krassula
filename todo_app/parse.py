import requests
from bs4 import BeautifulSoup

class AbrikosParse(object):
	def __init__(self, url):
		self.url = url
        
	def product_parse(self):
		page = requests.get(self.url)
		htmls = page.text
		soup = BeautifulSoup(htmls)
		title = soup.h1.get_text()
		try:
			percent = soup.find('div', attrs={'class':'percent'}).get_text()
		except Exception:
			percent = 'Нет'
		try:
			price = soup.find('span', attrs={'class':'price_value'}).get_text()
		except Exception:
			price = 'Цена не указана'
		try:
			currency  = soup.find('span', attrs={'class':'price_currency'}).get_text()
		except Exception:
			currency = ''
		try:
			measure = soup.find('span', attrs={'class':'price_measure'}).get_text()
		except Exception:
			measure = ''
		try:
			manu = soup.find('p', attrs={'class':'country_detail'}).find_all('span')[1].b.get_text()
		except Exception:
			manu = 'Не указан'
		prices = price + currency +  measure
		results = ([('Название',title),('Цена', prices),('Производитель',manu),('Акция',percent)])
		return results
        
	def category_parse(self):
		page = requests.get(self.url)
		htmls = page.text
		soup = BeautifulSoup(htmls)
		title = soup.h1.get_text()
		number = len(soup.find_all('div', attrs={'class':'item_block'}))
		number_sales = len(soup.find_all('div', attrs={'class':'sticker_aktsiya'}))
		results = ([('Название',title),('Количество товаров:', number),('Товары по акции:', number_sales)])
		return results

	def site_parse(self):
		page = requests.get('https://www.abri-kos.ru/company/news/')
		htmls = page.text
		soup = BeautifulSoup(htmls)
		last_news = soup.find_all("a", attrs={'class':'dark_link'})[-1].get_text()
		page_news = requests.get('https://www.abri-kos.ru/company/news/?PAGEN_1=' + last_news)
		last_news = int(last_news) - 1 
		news = page_news.text
		soup2 = BeautifulSoup(news)
		count_last_news = len(soup2.find_all('div', attrs={'class':'wti'}))
		news = 6*last_news + int(count_last_news)
		page_sale = requests.get('https://www.abri-kos.ru/sale/nashi_spetspredlozheniya/')
		sales = page_sale.text
		soup3 = BeautifulSoup(sales)
		last_sales_n = soup3.find_all("a", attrs={'class':'dark_link'})[-1].get_text()
		page_sales = requests.get('https://www.abri-kos.ru/sale/nashi_spetspredlozheniya/?PAGEN_2=' + last_sales_n)
		last_sales_n = int(last_sales_n) - 1
		sale_text = page_sales.text
		soup4 = BeautifulSoup(sale_text)
		count_last_sales = len(soup4.find_all('div', attrs={'class':'catalog_item_wrapp'}))
		sale = 40*last_sales_n + int(count_last_sales)
		results = ([('Новости',news),('Акции',sale)])
		return results
    	

class FoodTorgParse(object):
	def __init__(self, url):
		self.url = url

	def product_parse(self):
		page = requests.get(self.url)
		htmls = page.text
		soup = BeautifulSoup(htmls)
		title = soup.h1.get_text()
		try:
			price = soup.find('span', attrs={'class':'price__val'}).get_text()
		except Exception:
			price = 'Цена не указана'
		results = ([('Название',title),('Цена', price)])
		return results
        
	def category_parse(self):
		page = requests.get(self.url)
		htmls = page.text
		soup = BeautifulSoup(htmls)
		title = soup.h1.get_text()
		number = len(soup.find_all('span', attrs={'class':'b-pagination__page'}))
		number_sales = len(soup.find_all('div', attrs={'class':'sticker_aktsiya'}))
		results = ([('Название',title),('Количество товаров:', number)])
		return results