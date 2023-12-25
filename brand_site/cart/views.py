from product.models import Product
from .cart import Cart
from django.views.generic import TemplateView
from django.http import *
import json
from django.core import serializers
from django.template.loader import render_to_string




def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print(f"\n\nNew_form: {product_id}\n\n")
        product = Product.objects.get(id=int(product_id))
        cart = Cart(request)
        
        cart.add(product=product)

        item_quantity = cart.get_total_len()

        product_json = serializers.serialize('json', [product])
        product_data = json.loads(product_json)[0]['fields']

        # Вернуть обновленный HTML в качестве ответа JsonResponse
        return JsonResponse({'success': True, 'product_instance': product_data, 'quantity': item_quantity})


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
        print(f"\n\n{product_id}\n\n")
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product=product)
        cart_quantity = cart.get_total_len()
        print(f"\n\n{cart_quantity}\n\n")
        return JsonResponse({'success': True, 'cart_quantity': cart_quantity})


def delete_all_certain_product(request):
    product_id = request.POST.get('product_id')

    product = Product.objects.get(id=product_id)
    
    cart = Cart(request)

    cart.delete_all_certain_products(product) 

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_quantity = cart.get_total_len()
        
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=int(product_id))
        
        if cart.get_product_quantity(product_id) == 1:
            return JsonResponse({'success': False, 'message': 'Нельзя удалить последний товар'})
        
        cart.remove(product) 
        
    return JsonResponse({'success': True, 'cart_quantity': cart_quantity})


def delete_all(request):
    cart = Cart(request)
    cart.clear()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CartDetail(TemplateView):
    template_name = 'cart.html'
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.first() 
        cart = Cart(self.request)
        data['product'] = product
        data['cart'] = cart
        return data

