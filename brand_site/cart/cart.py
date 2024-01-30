from decimal import Decimal
from django.conf import settings
from product.models import Product
from django.shortcuts import get_object_or_404



class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def current_quantity(self, product_id):
        keys = self.cart.keys()
        for key in keys:
            if int(product_id) == int(key):
                return self.cart[key]["quantity"]
        return 0
            

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    

    def delete_all_certain_products(self, product):
        product_id = str(product.id)
        del self.cart[product_id]
        self.save()
    

    def remove(self, product, quantity=1):
        product_id = str(product.id)
        
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] <= quantity:
                del self.cart[product_id]
            else:
                self.cart[product_id]['quantity'] -= quantity

        self.save()


    def save(self):
        self.session.modified = True


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item.get('price', 0)) 
            item['total_price'] = item['price'] * item['quantity']
            yield item
    

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    

    def get_total_len(self):
        total_len = 0
        for item in self.cart.values():
            total_len += item['quantity']
        return total_len
    

    def get_product_quantity(self, prod_id):
        products = self.cart.items()
        count = 0
        
        for product in products:
            if int(product[0]) == int(prod_id):
                count = product[1]['quantity']
                break 
        return int(count)


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


    def get_content(self):
        return self.cart.items()
    

    def get_all_items(self):
        total = 0
        for item in self.cart:
            total += self.cart[item]['quantity']
        return total
    
    def get_products(self):
        return len(self.cart.keys())
