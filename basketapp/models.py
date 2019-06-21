from django.db import models
from django.conf import settings
from mainapp.models import Product

class Basket (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default= 0 )
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add= True )
    
    def product_cost(self):
        return self.product.price * self.quantity
    
    def total_quantity(self):
        return sum([el.quantity for el in self.user.basket.all()])
    
    def total_cost(self):
        return sum([el.product_cost() for el in self.user.basket.all()])
    