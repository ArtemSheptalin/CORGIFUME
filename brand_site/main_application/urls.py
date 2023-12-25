from django.urls import path
from .views import *
from cart.views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('catalog/', CatalogPageView.as_view(), name='services'),
    path('blog/', BlogPageView.as_view(), name='blog'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('brands/', BrandsPageView.as_view(), name='brands'),
    path('cosmetics/', CosmeticsPageView.as_view(), name='cosmetics'),
    path('catalog/', CatalogPageView.as_view(), name='catalog'),
    path('add-to-cart/', add_to_cart, name='add_cart'),
    path('add-certain-amount/', add_certain_amount, name='add_certain'),
    path('remove/', cart_remove, name='remove_cart'),
    path('delete_certain_product/', delete_all_certain_product, name="delete_product"),
    path('delete-cart/', delete_all, name="clear-cart"),
    path(r'^product-card/(?P<slug>[-\w]+)/$', ProductCardView.as_view(), name='product'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
]