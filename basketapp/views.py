from basketapp.models import Basket
from mainapp.models import Product
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def index(request):
    context = {
        'basket': request.user.basket.all()
    }
    return render(request, 'basketapp/index.html', context)

@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product', kwargs={'pk': pk}))
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    
    return HttpResponseRedirect(reverse('basket:index'))

@login_required
def update(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = Basket.objects.filter(pk=pk).first()
        if basket and quantity > 0:
            basket.quantity = quantity
            basket.save()
        elif basket and quantity == 0:
            basket.delete()
        else:
            return JsonResponse({'result': None})

        basket = request.user.basket.all()
        result = render_to_string('basketapp/includes/inc__basket_list.html',
                                  context={'basket': basket})

        return JsonResponse({'result': result})
 