from django.urls import path

from . import views

urlpatterns = [
    path('current', views.current, name='current'),
    path('history', views.history, name='history'),
    path('convert', views.convert, name='convert'),
    path('buy', views.buy, name='buy'),
]
