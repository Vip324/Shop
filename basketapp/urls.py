from django.urls import path, re_path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    re_path(r'^$', basketapp.index, name='index'),
    re_path(r'^add/(?P<pk>\d+)/$', basketapp.add, name='add'),
    re_path(r'^update/(?P<pk>\d+)/(?P<quantity>\d+)/$', basketapp.update),
    re_path(r'^delete/(?P<pk>\d+)/$', basketapp.delete, name='delete'),
    
]