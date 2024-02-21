from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main_application.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('blog/', include("blog.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




