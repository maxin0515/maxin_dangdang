from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from home_page_app.models import Category, Book, Address, Order


def index_page(request):
    return render(request, 'management/index.html')


def add_page(request):
    subcategory = Category.objects.filter(parent_id__isnull=False)
    return render(request, 'management/main/add.html', {"subcategory": subcategory})


def dzlist_page(request):
    order_list = Order.objects.all()
    num = request.GET.get("num")
    if num:
        num = int(num)
    else:
        num = 1
    page = Paginator(object_list=order_list, per_page=5).page(num)
    return render(request, 'management/main/dzlist.html', {"page": page, "amount": len(order_list)})


def list_page(request):
    num = request.GET.get("num")
    if num:
        num = int(num)
    else:
        num = 1
    books = Book.objects.all()
    page = Paginator(object_list=books, per_page=8).page(num)
    return render(request, 'management/main/list.html', {"page": page, "book_num": len(books)})


def splb_page(request):
    category_list = Category.objects.all()
    num = request.GET.get("num")
    if num:
        num = int(num)
    else:
        num = 1
    page = Paginator(object_list=category_list, per_page=8).page(num)
    return render(request, 'management/main/splb.html', {"page": page, "amount": len(category_list)})


def test_page(request):
    return render(request, 'management/main/test.html')


def zjsp_page(request):
    category_name = request.GET.get("category_name")
    if category_name:
        Category(category_name=category_name).save()
    return render(request, 'management/main/zjsp.html')


def zjzlb_page(request):
    category_list = Category.objects.filter(parent_id__isnull=True)
    for i in category_list:
        print(i.category_name)
    return render(request, 'management/main/zjzlb.html', {"category_list": category_list})


def add_subcategory_ajax(request):
    subcategory_name = request.GET.get("subcategory_name")
    category_id = request.GET.get("category_id")
    Category(category_name=subcategory_name, parent_id=int(category_id)).save()
    return JsonResponse({"OK": "OK"})


# 增加书籍的ajax
def add_book_ajax(request):
    book_name = request.POST.get("book_name")
    book_author = request.POST.get("book_author")
    publishing_house = request.POST.get("publishing_house")
    subcategory = int(request.POST.get("subcategory"))
    publication_time = request.POST.get("publication_time")
    shelves_date = request.POST.get("shelves_date")
    Book(book_name=book_name, book_author=book_author, publishing_house=publishing_house,
         publication_time=publication_time, book_category_id=subcategory, shelves_date=shelves_date).save()
    return JsonResponse({"OK": "OK"})


# 删除书籍
def book_delete_ajax(request):
    book_id = request.GET.get("book_id")
    book_id = book_id.split(",")
    print(book_id)
    # books = Book.objects.all()
    # page = Paginator(object_list=books, per_page=5).page(num)
    for i in book_id:
        print(int(i))
        Book.objects.filter(book_id=i).delete()
    return redirect('management:list')

# 删除订单
def order_delete(request):
    order_id = request.GET.get("order_id")
    order_id = order_id.split(",")
    print(order_id)
    # books = Book.objects.all()
    # page = Paginator(object_list=books, per_page=5).page(num)
    for i in order_id:
        print(int(i))
        Order.objects.filter(order_id=i).delete()
    return redirect('management:dzlist')