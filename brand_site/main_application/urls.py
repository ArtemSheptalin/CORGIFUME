from django.urls import path
from .views import MainPageView, CatalogPageView, BlogPageView, ContactsPageView, BrandsPageView, \
CosmeticsPageView, DiscountsPageView
from cart.views import add_to_cart, cart_remove


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('catalog/', CatalogPageView.as_view(), name='services'),
    path('blog/', BlogPageView.as_view(), name='blog'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('brands/', BrandsPageView.as_view(), name='brands'),
    path('cosmetics/', CosmeticsPageView.as_view(), name='cosmetics'),
    path('discounts/', DiscountsPageView.as_view(), name='discounts'),
    path('add-to-cart/', add_to_cart, name='add_cart'),
    path('remove/', cart_remove, name='remove_cart'),
]