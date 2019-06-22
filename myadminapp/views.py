from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from myadminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, AdminProductCategoryUpdateForm, AdminProductUpdateForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    context = {
        'title': 'Users',
        'object_list': ShopUser.objects.all().order_by('-is_active', '-is_superuser')
    }
    return render(request, 'myadminapp/index.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = AdminShopUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = AdminShopUserCreateForm()

    context = {
        'title': 'Users/Create',
        'form': form
    }
    return render(request, 'myadminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'Users/Edit',
        'form': form
    }
    return render(request, 'myadminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('myadmin:index'))

    context = {
        'title': 'Users/Delete',
        'user_to_delete': user}

    return render(request, 'myadminapp/user_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_recover(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('myadmin:index'))

    context = {
        'title': 'Users/Recover',
        'user_to_recover': user}

    return render(request, 'myadminapp/user_recover.html', context)



@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'title': 'Categories',
        'object_list': ProductCategory.objects.all()
    }
    return render(request, 'myadminapp/productcategory_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def productcategory_create(request):
    if request.method == 'POST':
        form = AdminProductCategoryUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = AdminProductCategoryUpdateForm()

    context = {
        'title': 'Categories/Create',
        'form': form
    }
    return render(request, 'myadminapp/productcategory_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def productcategory_update(request, pk):
    obj = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = AdminProductCategoryUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = AdminProductCategoryUpdateForm(instance=obj)

    context = {
        'title': 'Categories/Edit',
        'form': form
    }
    return render(request, 'myadminapp/productcategory_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def productcategory_delete(request, pk):
    obj = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse('myadmin:categories'))

    context = {
        'title': 'Category/Delete',
        'obj_to_delete': obj}

    return render(request, 'myadminapp/category_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def productcategory_recover(request, pk):
    obj = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        obj.is_active = True
        obj.save()
        return HttpResponseRedirect(reverse('myadmin:categories'))

    context = {
        'title': 'Category/Recover',
        'obj_to_recover': obj}

    return render(request, 'myadminapp/category_recover.html', context)

@user_passes_test(lambda u: u.is_superuser)
def products(request, category_pk):
    cat_obj = get_object_or_404(ProductCategory, pk=category_pk)
    context = {
        'title': 'Products',
        'category': cat_obj,
        'object_list': cat_obj.product_set.all()
    }
    return render(request, 'myadminapp/product_list.html', context)

def product_read (request, pk):
    content = {
        'title' : 'product/details',
        'object' : get_object_or_404(Product, pk=pk),
    }
    return render(request, 'myadminapp/product_read.html' , content)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, category_pk):
    cat_obj = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products',
                                                kwargs={'category_pk': category_pk}))
    else:
        form = AdminProductUpdateForm(initial={'category': cat_obj})

    context = {
        'title': 'продукты/создание',
        'form': form,
        'category': cat_obj,
    }
    return render(request, 'myadminapp/product_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products',
                                                kwargs={'category_pk': obj.category.pk}))
    else:
        form = AdminProductUpdateForm(instance=obj)

    context = {
        'title': 'product/edit',
        'form': form,
        'category': obj.category,
    }
    return render(request, 'myadminapp/product_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse('myadmin:products',
                                            kwargs={'category_pk': obj.category.pk}))

    context = {
        'title': 'product/delete',
        'obj_to_delete': obj}

    return render(request, 'myadminapp/product_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_recover(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = True
        obj.save()
        return HttpResponseRedirect(reverse('myadmin:products',
                                            kwargs={'category_pk': obj.category.pk}))

    context = {
        'title': 'product/recover',
        'obj_to_recover': obj}

    return render(request, 'myadminapp/product_recover.html', context)
