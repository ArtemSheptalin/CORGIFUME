from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'image_show', 'price', 'available', 'created']
    list_filter = ['available', 'created']
    list_editable = ['price', 'available']
    # prepopulated_fields = {'id': ('name', )}

    def image_show(self, obj):
        if obj.image.first():
            return mark_safe("<img src='{}' width='60' />".format(obj.image.first()))
        return "None"

    image_show.__name__ = "Картинка"

admin.site.register(Image)




