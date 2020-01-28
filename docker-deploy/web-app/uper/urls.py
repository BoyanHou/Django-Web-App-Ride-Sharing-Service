from django.urls import path

from . import views

app_name = 'uper'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register_page/', views.register_page, name='register_page'),
    path('register_process/', views.register_process, name='register_process'),
]

