from django.db import models
from suppliers.models import Supplier
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Products(models.Model):
    product_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)                                                   

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField(null=False, blank=False)
    minimum_order_quantity = models.CharField(max_length=250)
    featured = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('product_name',)
        index_together = (('id', 'slug'),)


    def __str__(self):
        return self.product_name


    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id,self.slug])



