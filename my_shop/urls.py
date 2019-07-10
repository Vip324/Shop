from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

#import mainapp.views as mainapp

urlpatterns = [
    re_path(r'^', include('mainapp.urls', namespace='main')),

    re_path(r'^', include('social_django.urls', namespace='social')),
    
    re_path( r'^auth/' , include('authapp.urls', namespace='auth')),
    re_path( r'^basket/', include('basketapp.urls', namespace='basket')),
    re_path(r'^myadmin/', include('myadminapp.urls', namespace='myadmin')),

    re_path(r'^order/', include('ordersapp.urls', namespace='order')),
    
    path( 'admin/' , admin.site.urls),
] 

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [re_path( r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
