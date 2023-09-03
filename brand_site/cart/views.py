from django.http import JsonResponse
from django.shortcuts import redirect
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


def add_to_cart(request):
    cart = Cart(request)
    product = Product.objects.get(id=1)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request):
    product_id = 1 
    quantity_to_remove = 1 
    
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product, quantity=quantity_to_remove) 

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class CartDetail(TemplateView):
    template_name = '/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/cart/templates/cart/cart.html'
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.first() 
        cart = Cart(self.request)
        data['product'] = product
        data['cart'] = cart
        return data

