from typing import Any, Dict
from django.views.generic import TemplateView
from product.models import Product
from cart.cart import Cart


class MainPageView(TemplateView):
    template_name = 'main_page.html'


class CatalogPageView(TemplateView):
    template_name = 'services.html'


class BlogPageView(TemplateView):
    template_name = 'cases.html'


class ContactsPageView(TemplateView):
    template_name = 'contacts.html'


class BrandsPageView(TemplateView):
    template_name = 'brands.html'


class CosmeticsPageView(TemplateView):
    template_name = 'cosmetics.html'


class DiscountsPageView(TemplateView):
    
    template_name = 'discounts.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.first() 
        data['product'] = product
        return data

        
        
        