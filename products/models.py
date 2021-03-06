from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    @property
    def avarage(self):
        ratings = [review.rating for review in self.reviews.all()]
        if len(ratings)> 0:
            avarage = sum (ratings) / len(ratings)
        else:
            avarage = 0
        #avarage = sum (ratings) / len(ratings)
        avarage = round(avarage, 1)
        return avarage

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", null=True)
    timestamp = models.DateTimeField(auto_now_add= True, null=True)
