from django.db import models

from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'Cancel'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    status = models.CharField(verbose_name='Status', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='Acniv', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return 'Current order: {}'.format(self.id)

    def get_total_quantity(self):
        # Сколько всего количества товаров
        items = self.orderitems.select_related()
        # for item in items:
        #     s+= item.quantity
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        # Скольо всего товаров
        items = self.orderitems.select_related()
        # items = self.orderitems.count()
        return len(items)

    def get_total_cost(self):
        # Стоймость всех товаров
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    # Товар который мы купили
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    # количество
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
