from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm
from django.contrib import auth
from django.urls import reverse

def login(request):
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
        
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST[ 'next' ])
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()
       
    content = {
        'title': 'LOGIN',
        'form': form,
        'next': next,
    }
    return render(request, 'authapp/login.html', content)
    
def logout (request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopUserRegisterForm()

    content = {
        'title': 'REGISTRATION',
        'form': form
    }
    return render(request, 'authapp/register.html', content)

def edit(request):
    if request.method == 'POST':
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
            # return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserEditForm(instance=request.user)

    content = {
        'title': 'EDIT',
        'form': form
    }

    return render(request, 'authapp/edit.html', content)
