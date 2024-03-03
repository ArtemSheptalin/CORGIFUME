from typing import Any

from django.db.models.query import QuerySet

from cart.cart import Cart
from django.views.generic import *
from product.models import *
from django.db.models import FloatField
from django.db.models.functions import Cast
import json
from django.core import serializers
from django.http import *
from django.db.models import Q
from utils.utils import *

class MainPageView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
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

        return JsonResponse({'success': True, 'product_instance': product_data, 
                             'quantity': item_quantity, 'new_cart': card_data, 
                             'id': product_id})

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.first() 
        cart = Cart(self.request)
        data['product'] = product
        data['cart'] = cart
        for key, value in self.request.session.items():
            print(f"\nKey: {key}, Value: {value}\n")
        # print(f"\n{self.request.session.keys()}\n")
        return data
    
    

class CatalogPageView(TemplateView):
    template_name = 'services.html'


class BlogPageView(TemplateView):
    template_name = 'cases.html'


class ContactsPageView(TemplateView):
    template_name = 'contacts.html'


class BrandsPageView(TemplateView):
    template_name = 'brands.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        brands_list = []
        dictionary = {}

        data = super().get_context_data(**kwargs)
        brands = Product.objects.values('brand').distinct()

        for brand in brands:
            brands_list.append(brand['brand'])

        for each_brand in sorted(set(brands_list), reverse=False):
            initial = each_brand[0]
            if initial not in dictionary:
                dictionary[initial] = [] 
            dictionary[initial].append(each_brand) 


        data['brands'] = dictionary
        data['letters'] = ['1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return data


class CosmeticsPageView(TemplateView):
    template_name = 'cosmetics.html'


class CatalogPageView(ListView):
    
    template_name = 'catalog.html'
    model = Product
    paginate_by = 30 

    def get_context_data(self, *args, **kwargs):

        data = super().get_context_data(**kwargs)

        brands = Product.objects.order_by('brand').values_list('brand', flat=True).distinct()

        string_brands = Product.objects.order_by('brand').values_list('brand', flat=True).distinct()

        data['brands'] = sorted(set(brands), reverse=False)
        data['string_brands'] = str(string_brands)
        data['selected_brands'] = self.request.GET.getlist('brand')
        data['selected_ml'] = self.request.GET.getlist('mls')
        data['selected_parfums'] = self.request.GET.getlist('parfum')

        data['selected_min_price'] = self.request.GET.get('superscroll1')
        data['selected_max_price'] = self.request.GET.get('superscroll2')
        
        queryset = self.get_queryset()
        
        if queryset:
            data['total_query_count'] = queryset.count()
        else:
            data['total_query_count'] = 0


        return data
    
    def get_queryset(self):
        queryset = super().get_queryset()
        brands = self.request.GET.getlist('brand')
        mls = self.request.GET.get('mls')
        parfums = self.request.GET.getlist('parfum')
        min_price = self.request.GET.get('superscroll1')
        max_price = self.request.GET.get('superscroll2')
        search_box = self.request.GET.get('search')
        expensive = self.request.GET.get('Сначала дорогие')
        cheapest = self.request.GET.get('Сначала дешевые')


        if expensive == 'Сначала дорогие':
            queryset = Product.objects.order_by('-price')
        
        if cheapest == 'Сначала дешевые':
            queryset = Product.objects.order_by('price')



        if search_box:
            queryset = Product.objects.filter(Q(name__icontains=search_box) 
                                              | Q(brand__icontains=search_box) 
                                              | Q(parfum_type__icontains=search_box)
                                              | Q(notes__icontains=search_box)
                                              | Q(inner_article__icontains=search_box))

        if brands:
            queryset = queryset.filter(brand__in=brands)


        if mls:
            if mls == '30':
                queryset = queryset.filter(ml__lte=30)
            elif mls == '50':
                queryset = queryset.filter(ml__gt=30, ml__lte=50)
            elif mls == '75':
                queryset = queryset.filter(ml__gt=50, ml__lte=75)
            elif mls == '100':
                queryset = queryset.filter(ml__gt=75, ml__lte=100)
            elif mls == '101':
                queryset = queryset.filter(ml__gt=100)
        
        if parfums:
            queryset = Product.objects.filter(parfum_type__in=parfums)

        
        if min_price:
            min_price = min_price.replace(" ", "")
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            max_price = max_price.replace(" ", "")
            queryset = queryset.filter(price__lte=max_price)
        
        if not queryset:
            queryset = [] 

        return queryset


class ProductCardView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_object(self,queryset=None):
        id = self.kwargs.get('id')
        return self.model.objects.get(id=id)
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        
        id = self.kwargs.get('id')
        
        current_product = Product.objects.get(id=id)
        products = Product.objects.filter(name=current_product.name).order_by('ml')

        data['products'] = list(products.values_list('ml', flat=True).distinct())
        data['sizes'] = products.values_list('price', flat=True)
        data['length_size'] = len(list(products.values_list('ml', flat=True).distinct()))

        amount = cart.current_quantity(id)      
        
        data['amount'] = amount 
        
        return data
        


class AboutUsView(TemplateView):
    template_name = 'about.html'


class CatalogQuerysetBrand(ListView):
    template_name = 'catalog.html'
    model = Product
    paginate_by = 30 

    def get_queryset(self):
        queryset =  super().get_queryset()
        brand = self.kwargs['link_brand']  # Получаем название бренда из id
        queryset = queryset.filter(brand=brand) 
        return queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        brands = Product.objects.order_by('brand').values_list('brand', flat=True).distinct()
        string_brands = Product.objects.order_by('brand').values_list('brand', flat=True).distinct()
        data['brands'] = sorted(set(brands), reverse=False)
        data['string_brands'] = str(string_brands)
        data['total_query_count'] = self.get_queryset().count()
        return data


class ConditionsView(TemplateView):
    template_name = 'conditions.html'


class RequisitesView(TemplateView):
    template_name = 'requisites.html'


class PoliticsView(TemplateView):
    template_name = 'politics.html'
    

    


    






        
        
        