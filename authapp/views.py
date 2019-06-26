from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse

from authapp.models import ShopUser


def send_verify_mail(user):
    link = reverse('auth:verify', kwargs={'email': user.email, 'activation_key': user.activation_key})
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке: {settings.DOMAIN_NAME}{link} '

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently= False )



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
            user = form.save()
            if send_verify_mail(user):
                print( 'E-mail was send!' )
            else :
                print( 'Error E-mail send' )
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserRegisterForm()

    content = {
        'title': 'REGISTRATION',
        'form': form
    }
    return render(request, 'authapp/register.html', content)

@transaction.atomic
def edit(request):
    if request.method == 'POST':
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
            # return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {
        'title': 'EDIT',
        'form': form,
        'profile_form' : profile_form
    }

    return render(request, 'authapp/edit.html', content)

def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expire():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print( f'error activation user: {user} ' )
            return render(request, 'authapp/verification.html')

    except Exception as e:
        print( f'error activation user : {e.args} ' )
        return HttpResponseRedirect(reverse('main:index'))
