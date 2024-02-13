from utils.utils import UtilitiesFunctions
from product.models import Product
from .cart import Cart
from django.views.generic import TemplateView
from django.http import *
import json
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=int(product_id))
        cart = Cart(request)
        
        cart.add(product=product)

        item_quantity = cart.get_total_len()

        product_json = serializers.serialize('json', [product])
        product_data = json.loads(product_json)[0]['fields']

        card_data = {
            'items': list(cart.get_content()),
            'subtotal': cart.get_total_price(),
        }

        return JsonResponse({'success': True, 'product_instance': product_data, 'quantity': item_quantity, 'new_cart': card_data, 'id': product_id})


def add_product(request):
    if request.method == 'POST':
        # utilities_object = UtilitiesFunctions(request.user)
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        
        cart = Cart(request)
        cart.add(product=product)
        
        cart_quantity = cart.get_all_items()
        product_amount = cart.get_product_quantity(product.id)
        total_price = cart.get_total_price()

        current_price = product_amount * product.price
        # product_bonuses = utilities_object.showing_income_balls(int(current_price))

        return JsonResponse({'success': True, 'cart_quantity': cart_quantity,
                             'price': product.price, 'product_amount': product_amount,
                             'total_price': total_price})


def add_certain_amount(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        utilities_object = UtilitiesFunctions(request.user)
        cart = Cart(request)
        cart.add(product=product)
        
        cart_quantity = cart.get_all_items()
        product_amount = cart.get_product_quantity(product.id)
        total_price = cart.get_total_price()
        bonuses = utilities_object.showing_income_balls(int(total_price))
        product_bonuses = utilities_object.showing_income_balls(int(product.price * product_amount))
        return JsonResponse({'success': True, 'cart_quantity': cart_quantity,
                             'price': product.price, 'product_amount': product_amount,
                             'total_price': total_price, 'bonuses': bonuses, 'product_bonuses': product_bonuses})


def delete_all_certain_product(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        cart = Cart(request)
        content_cart = cart.get_content()
        cart.delete_all_certain_products(product)
        cart_quantity = cart.get_all_items()
        total_price = cart.get_total_price()
        content_cart = list(content_cart)

        return JsonResponse({'success': True, 'product_id': product.id, 
                             'content_cart': content_cart, 'total_price': total_price, 
                             'cart_quantity': cart_quantity})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def cart_remove(request):
    if request.method == 'POST':
        cart = Cart(request)
        
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=int(product_id))
        

        if cart.get_product_quantity(product_id) > 0:
            cart.remove(product)
            product_amount = cart.get_product_quantity(product.id)
            total_price = cart.get_total_price()
            cart_quantity = cart.get_total_len()
            return JsonResponse({'success': True, 'cart_quantity': cart_quantity,
                             'price': product.price, 'product_amount': product_amount,
                             'total_price': total_price})

        elif cart.get_product_quantity(product_id) == 0:
            cart.delete_all_certain_content
            return JsonResponse({'success': False, 'message': 'Невозможно иметь отрицательное число товара!'})


def cart_remove_second(request):
    if request.method == 'POST':
        cart = Cart(request)

        utilities_object = UtilitiesFunctions(request.user)
        
        product_id = request.POST.get('product_id')
        
        product = Product.objects.get(id=int(product_id))
        
        
        if cart.get_product_quantity(product_id) == 1:
            return JsonResponse({'success': False, 'message': 'Невозможно иметь нулевое число товара!'})
        else:
            cart.remove(product)
            current_price = int(request.POST.get('current_price')) - int(product.price)
            product_amount = cart.get_product_quantity(product.id)
            total_price = cart.get_total_price()
            cart_quantity = cart.get_total_len()
            bonuses = utilities_object.showing_income_balls(int(total_price))
            product_bonuses = utilities_object.showing_income_balls(int(current_price))
            
            return JsonResponse({'success': True, 'cart_quantity': cart_quantity,
                             'price': product.price, 'product_amount': product_amount,
                             'total_price': total_price, 'bonuses': bonuses, 'product_bonuses': product_bonuses})
    


def delete_all(request):
        
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()
        cart_quantity = cart.get_total_len()
        return JsonResponse({'success': True, 'cart_quantity': cart_quantity})


class CartDetail(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users:login')
    template_name = 'cart.html'
    
    def get_context_data(self, *args, **kwargs):

        data = super().get_context_data(**kwargs)
        utilities_object = UtilitiesFunctions(self.request.user)
        cart = Cart(self.request)
        # current_price = self.request.POST.get('current_price')
        
        data['cart'] = cart
        # data['product_bonuses'] = utilities_object.showing_income_balls(int(current_price))
        data['total_bonuses_counter'] = utilities_object.showing_income_balls(int(cart.get_total_price()))

        contents = cart.get_content()
        ids = [key for key, _ in contents]

        image_contents = Product.objects.filter(id__in=ids).prefetch_related('image')

        images = []
        for prod in image_contents:
            current_price = prod.price
            first_image = prod.image.first()
            print(f"\n{int(current_price)}\n")
            
            if first_image:
                images.append(first_image)
        data['product_bonuses'] = utilities_object.showing_income_balls(int(current_price))
        data['contents'] = contents
        data['images'] = images

        return data

