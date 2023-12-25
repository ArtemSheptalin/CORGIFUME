from typing import Any

from cart.cart import Cart
from django.views.generic import *
from product.models import *
from django.db.models import FloatField
from django.db.models.functions import Cast
import re




class MainPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.first() 
        cart = Cart(self.request)
        data['product'] = product
        data['cart'] = cart
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
        data['total_query_count'] = self.get_queryset().count()

        return data
    
    def get_queryset(self):
        queryset = super().get_queryset()
        brands = self.request.GET.getlist('brand')
        mls = self.request.GET.getlist('mls')
        parfums = self.request.GET.getlist('parfum')
        min_price = self.request.GET.get('superscroll1')
        max_price = self.request.GET.get('superscroll2')

        if brands:
            queryset = queryset.filter(brand__in=brands)

        if mls:
            if mls[0] == '30':
                queryset = queryset.extra(where=["CAST(ml AS float) < 30"])
            elif mls[0] == '50':
                queryset = queryset.annotate(ml_float=Cast('ml', output_field=FloatField())).filter(ml_float__gt=30, ml_float__lt=51)
            elif mls[0] == '75':
                queryset = queryset.annotate(ml_float=Cast('ml', output_field=FloatField())).filter(ml_float__gt=51, ml_float__lt=75)
            elif mls[0] == '100':
                queryset = queryset.annotate(ml_float=Cast('ml', output_field=FloatField())).filter(ml_float__gt=75, ml_float__lt=100)
            elif mls[0] == '101':
                queryset = queryset.extra(where=["CAST(ml AS float) > 100"])
        
        if parfums:
            matching_ids = []
            all_products = Product.objects.all().prefetch_related('image')
            for product in all_products:
                image_name = product.image.first()
                if parfums[0] in str(image_name):
                    matching_ids.append(product.id)

            queryset = queryset.filter(id__in=matching_ids)
        
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
        slug = self.kwargs.get('slug')
        return self.model.objects.get(slug=slug)
    
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        name = self.kwargs.get('slug')
        cleaned_name = name.split('tester')
        if 'not-' in cleaned_name[0]:
            cleaned_name = cleaned_name[0].replace('-not-', '')
            cleaned_name = cleaned_name.replace('-', ' ')
            cleaned_name = cleaned_name.title()
            if 'Vip' in cleaned_name:
                cleaned_name = cleaned_name.replace('Vip', 'VIP')
            elif 'Xs' in cleaned_name:
                cleaned_name = cleaned_name.replace('Xs', 'XS')
        else:
            cleaned_name = cleaned_name[0].rstrip('-')
            cleaned_name = cleaned_name.replace('-', ' ')
            cleaned_name = cleaned_name.title()
            if 'Vip' in cleaned_name:
                cleaned_name = cleaned_name.replace('Vip', 'VIP')
            elif 'Xs' in cleaned_name:
                cleaned_name = cleaned_name.replace('Xs', 'XS')
        products = Product.objects.filter(name=cleaned_name).order_by('ml')
        data['products'] = list(products.values_list('ml', flat=True).distinct())
        return data


class AboutUsView(TemplateView):
    template_name = 'about.html'





        
        
        