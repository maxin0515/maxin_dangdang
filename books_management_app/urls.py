from django.urls import path

from . import views

urlpatterns = [
    path("index_page/",views.index_page,name="index"),
    path("add_page/",views.add_page,name="add"),
    path("dzlist_page/",views.dzlist_page,name="dzlist"),
    path("list_page/",views.list_page,name="list"),
    path("splb_page/",views.splb_page,name="splb"),
    path("test_page/",views.test_page,name="test"),
    path("zjsp_page/",views.zjsp_page,name="zjsp"),
    path("zjzlb_page/",views.zjzlb_page,name="zjzlb"),
    path("add_book_ajax/",views.add_book_ajax,name="add_book_ajax"),
    path("book_delete_ajax/",views.book_delete_ajax,name="book_delete_ajax"),
    path("add_subcategory_ajax/",views.add_subcategory_ajax,name="add_subcategory_ajax"),
    path("order_delete/",views.order_delete,name="order_delete"),
]
