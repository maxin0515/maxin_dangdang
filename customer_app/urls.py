from django.urls import path

from . import views

urlpatterns = [
    path('login/page/', views.login_page, name='login'),
    path('register/page/', views.register_page, name='register'),
    path('register/username_confirm/', views.register_username_confirm, name='username_confirm'),
    path('register/captcha_confirm/', views.register_captcha_confirm, name='captcha_confirm'),
    path('register/logic/', views.register_logic, name='register_logic'),
    path('register/ok/', views.register_ok_page, name='register_ok'),
    path('login/logic/', views.login_logic, name='login_logic'),
    path('log_out/', views.log_out, name='log_out'),

]
