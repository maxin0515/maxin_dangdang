from django.urls import path

from . import views

urlpatterns = [
    path('show_ajax/', views.shopping_cart_ajax, name='show_ajax'),
    # 清空购物车的路径，待删除
    path('clear/', views.clear_session, name='clear'),
    path('change_amount/', views.book_amount, name='change_amount'),
    path('show/', views.shopping_cart, name='show'),
    path('indent/', views.login_state_logic, name='indent'),
    path('indent_ok/', views.indent_ok, name='indent_ok'),
    path('del_book/', views.del_book_form_shoppong_cart, name='del_book'),
    path('login_state_confirm/',views.login_state_logic, name='confirm_login_state'),
    path('address_query/', views.address_query, name='address_query'),
    path('address_save/', views.address_save, name='address_save'),
]
