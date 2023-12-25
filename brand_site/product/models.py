from django.db import models


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

    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    upper_notes = models.CharField(null=True)
    medium_notes = models.CharField(null=True)
    lower_notes = models.CharField(null=True)
    year = models.CharField(null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)
    brand = models.CharField(null=True)
    ml = models.CharField(null=True)
    tester = models.BooleanField(default=False)
    top_season = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    orders_amount = models.CharField(default=0)
    color = models.CharField(null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return  self.name


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    image = models.CharField()

    def __str__(self):
        return f"{self.image}"