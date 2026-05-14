from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('train/', views.train, name='train'),
    path('reset/', views.reset_train, name='reset'),
    path('stats/', views.stats, name='stats'),
    path('add/', views.add_word, name='add'),
]