from product.models import Product
from .cart import Cart
from django.views.generic import TemplateView
from django.http import *
import json
from django.core import serializers


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


        # category_json = serializers.serialize('json', [product.category])
        # category_data = json.loads(category_json)[0]['fields']

        # image_json = serializers.serialize('json', [product.image.first()])
        # image_data = json.loads(image_json)[0]['fields']

        # return JsonResponse({'success': True, 'item_quantity': cart_quantity,
        #         'item_name': product.name, 'item_category': category_data['name'], 
        #         'item_ml': product.ml, 'item_price': product.price,
        #         'item_image': image_data['image']})



def add_certain_amount(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product=product)
        cart_quantity = cart.get_all_items()
        product_amount = cart.get_product_quantity(product.id)
        total_price = cart.get_total_price()
        return JsonResponse({'success': True, 'cart_quantity': cart_quantity,
                             'price': product.price, 'product_amount': product_amount,
                             'total_price': total_price})


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
        
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=int(product_id))
        
        if cart.get_product_quantity(product_id) == 1:
            return JsonResponse({'success': False, 'message': 'Невозможно иметь нулевое число товара!'})
        else:
            cart.remove(product)
            product_amount = cart.get_product_quantity(product.id)
            total_price = cart.get_total_price()
            cart_quantity = cart.get_total_len()
            return JsonResponse({'success': True, 'cart_quantity': cart_quantity,
                             'price': product.price, 'product_amount': product_amount,
                             'total_price': total_price})
    


def delete_all(request):
        
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()
        cart_quantity = cart.get_total_len()
        return JsonResponse({'success': True, 'cart_quantity': cart_quantity})


class CartDetail(TemplateView):
    template_name = 'cart.html'
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.first() 
        cart = Cart(self.request)
        data['product'] = product
        data['cart'] = cart

        contents = cart.get_content()
        ids = [key for key, _ in contents]

        image_contents = Product.objects.filter(id__in=ids).prefetch_related('image')

        images = []
        for prod in image_contents:
            first_image = prod.image.first()
            if first_image:
                images.append(first_image)

        data['contents'] = contents
        data['images'] = images

        return data

