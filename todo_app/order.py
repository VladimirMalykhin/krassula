from django.conf import settings


class Order(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.ORDERS_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.ORDERS_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, name, mail):
        product_id = 0
        self.cart[product_id] = {'name': name,
                                     'mail': mail}
        self.save()

    
    def save(self):
        self.session[settings.ORDERS_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True
        
    def remove(self):
      
        del self.cart[0]
        self.save()
          
    def ite(self):

        for item in self.cart.values():
            item['name'] = item['name']
            item['mail'] = item['mail'] 
            return item