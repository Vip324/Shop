from django.urls import path, re_path
import myadminapp.views as myadminapp

app_name = 'myadminapp'

urlpatterns = [
    re_path(r'^$', myadminapp.UsersListView.as_view(), name='index'),
    re_path(r'^user/create/$', myadminapp.user_create, name='user_create'),
    re_path(r'^user/update/(?P<pk>\d+)/$', myadminapp.user_update, name='user_update'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', myadminapp.user_delete, name='user_delete'),
    re_path(r'^user/recover/(?P<pk>\d+)/$', myadminapp.user_recover, name='user_recover'),

    re_path(r'^productcategories/$', myadminapp.categories, name='categories'),
    re_path(r'^productcategory/create/$', myadminapp.ProductCategoryCreate.as_view(), name='productcategory_create'),
    re_path(r'^productcategory/update/(?P<pk>\d+)/$', myadminapp.ProductCategoryUpdate.as_view(), name='productcategory_update'),
    re_path(r'^productcategory/delet/(?P<pk>\d+)/$', myadminapp.ProductCategoryDelete.as_view(), name='productcategory_delete'),
    re_path(r'^productcategory/recover/(?P<pk>\d+)/$', myadminapp.productcategory_recover, name='productcategory_recover'),

    re_path(r'^products/(?P<category_pk>\d+)/$', myadminapp.products, name='products'),
    re_path(r'^product/read/(?P<pk>\d+)/$', myadminapp.ProductDetail.as_view(), name='product_read'),
    re_path(r'^product/create/(?P<category_pk>\d+)/$', myadminapp.product_create, name='product_create'),
    re_path(r'^product/update/(?P<pk>\d+)/$', myadminapp.product_update, name='product_update'),
    re_path(r'^product/delete/(?P<pk>\d+)/$', myadminapp.product_delete, name='product_delete'),
    re_path(r'^product/recover/(?P<pk>\d+)/$', myadminapp.product_recover, name='product_recover'),
]
