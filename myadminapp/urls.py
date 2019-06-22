from django.urls import path, re_path
import myadminapp.views as myadminapp

app_name = 'myadminapp'

urlpatterns = [
    re_path(r'^$', myadminapp.index, name='index'),
    re_path(r'^user/create/$', myadminapp.user_create, name='user_create'),
    re_path(r'^user/update/(?P<pk>\d+)/$', myadminapp.user_update, name='user_update'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', myadminapp.user_delete, name='user_delete'),
    re_path(r'^user/recover/(?P<pk>\d+)/$', myadminapp.user_recover, name='user_recover'),

    re_path(r'^productcategories/$', myadminapp.categories, name='categories'),
    re_path(r'^productcategory/create/$', myadminapp.productcategory_create, name='productcategory_create'),
    re_path(r'^productcategory/update/(?P<pk>\d+)/$', myadminapp.productcategory_update, name='productcategory_update'),
    re_path(r'^productcategory/delet/(?P<pk>\d+)/$', myadminapp.productcategory_delete, name='productcategory_delete'),
    re_path(r'^productcategory/recover/(?P<pk>\d+)/$', myadminapp.productcategory_recover, name='productcategory_recover'),
]
