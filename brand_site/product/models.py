from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    parfum_type = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=200, null=True)
    notes = models.CharField(null=True, blank=True)
    year = models.CharField(null=True, blank=True)
    country = models.CharField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=50)
    ml = models.IntegerField(null=True, blank=True)
    tester = models.BooleanField(default=False)
    top_season = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    orders_amount = models.IntegerField(default=0)
    newest = models.BooleanField(default=False)
    article = models.CharField()
    inner_article = models.CharField(max_length=70)
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'name'), )
    

    def get_absolute_url(self):
        return reverse("product", kwargs={"id": self.id})
    

    def __str__(self):
        return  self.name


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='!ALL_IMAGES', max_length=500)

    class Meta:
        ordering = ('image',)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        index_together = (('id', 'image'), )

    def __str__(self):
        return self.image.url