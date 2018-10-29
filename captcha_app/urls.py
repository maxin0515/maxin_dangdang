from django.urls import path

from . import views

urlpatterns = [
    path('show/captcha/', views.get_captcha, name='show'),
]
