from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home_page, name='homepage'),
    path('book/category/', views.book_category_page, name='category'),
    path('book/information/', views.book_information, name='information')
]
