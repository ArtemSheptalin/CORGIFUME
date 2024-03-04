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
    path('catalog', CatalogPageView.as_view(), name='catalog'),
    path('catalog/<str:link_brand>/', CatalogQuerysetBrand.as_view(), name='brand_catalog'),    
    path('add-to-cart/', add_to_cart, name='add_cart'),
    path('add-certain-amount/', add_certain_amount, name='add_certain'),
    path('add-product/', add_product, name='add_product'),
    path('remove/', cart_remove, name='remove_cart'),
    path('remove_second/', cart_remove_second, name='remove_cart_second'),
    path('delete_certain_product/<int:id>/', delete_all_certain_product, name="delete_product"),
    path('delete-cart/', delete_all, name="clear-cart"),
    path('product-card/<int:id>/', ProductCardView.as_view(), name='product'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('cogifume-conditions/', ConditionsView.as_view(), name='conditions'),
    path('cogifume-requisites/', RequisitesView.as_view(), name='requisites'),
    path('cogifume-confidential-politicts/', PoliticsView.as_view(), name='politics'),
    path('cogifume-cookies/', CookiesView.as_view(), name='cookies'),
]