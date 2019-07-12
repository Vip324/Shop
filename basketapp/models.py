from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product


# Менеджер модели
class BasketQuerySet(models.QuerySet):
    # удаление набора данных
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super().delete(*args, **kwargs)

class Basket(models.Model):

    # 1. Переопределение базовго менеджера
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default= 0 )
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add= True )
    
    def product_cost(self):
        return self.product.price * self.quantity



    @cached_property
    def get_items_cached (self):
        return self.user.basket.select_related()

    def total_quantity(self):
        _items = self.get_items_cached
        return sum([el.quantity for el in _items])
    
    def total_cost(self):
        _items = self.get_items_cached
        return sum([el.product_cost() for el in _items])





    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product) \
 \
    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]

        return basket_items_dic

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    # переопределяем метод, удаляющий объект
    def delete(self):
        print('удаление объекта корзины') #?
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    def save(self, *args, **kwargs):
        # 1. Создали новый объект корзины
        # 2. Измененеие объекта

        # как понять изменяем объект или создаем? - pk
        if self.pk:
            # изменяем объект
            # 1. Сколько осталось в корзине
            # 2. Сколько было в корзине
            # print('сколько осталось в конризе:', self.quantity)

            # Где взять старое значение
            # print('сколько было (старое значение)', Basket.objects.get(pk=self.pk).quantity)
            # print('сколько было (старое значение)', self.__class__.get_item(self.pk).quantity)

            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            # создаем объект
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)
    