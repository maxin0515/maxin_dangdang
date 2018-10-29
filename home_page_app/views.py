import random

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from home_page_app.models import Category, Book


# Create your views here.

# 当当首页的跳转view,dangdang/home/
def home_page(request):
    # 接收用户昵称，如果有则认为是登录状态
    user_name = request.GET.get("user_name")
    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session is None:
        user_name = ""
    # 从数据库的分类表中查询所有数据
    book_categories = Category.objects.all()
    # 新建一个category1列表，存储所有的一级标题（parent_id为none的数据）
    category1 = []
    # 新建一个category2列表，存储所有的二级标题（parent_id不为空的数据）
    category2 = []
    # 遍历查询出来的数据分类
    for ele in book_categories:
        # 判断parent_id为空的数据
        if ele.parent_id is None:
            # 将parent_id为空的数据追加到category1列表中
            category1.append(ele)
        else:
            # 将parent_id不为空的数据追加到category2列表中
            category2.append(ele)

    # 从图书表中查询用户评分前十的书籍，用于主编推荐
    book_list_query_grade = Book.objects.all().order_by("-customer_sgrade")
    book_list_query_grade = book_list_query_grade[0:10]

    # 从图书表中查询上架时间最新的图书
    book_list_query_shelves_date = Book.objects.all().order_by("-shelves_date")
    # 从新书中查询销量前5名
    book_list_query_shelves_date_sales = Book.objects.filter(shelves_date__year=2018, shelves_date__month=9).order_by(
        '-sales')[:5]
    # 取前8本
    book_list_query_shelves_date = book_list_query_shelves_date[0:8]
    # 将html和category1与category2响应到浏览器
    return render(request, 'homepage/index_test.html',
                  {'category1': category1, 'category2': category2, 'book_list_query_grade': book_list_query_grade,
                   'book_list_query_shelves_date': book_list_query_shelves_date, 'book_list_query_shelves_date_sales':
                       book_list_query_shelves_date_sales, "user_name": user_name})


# 跳转到图书分类页面，dangdang/book/category/
def book_category_page(request):
    query = request.GET.get("query")
    print(query,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    user_name = request.GET.get("user_name")
    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session is None:
        user_name = ""

    # 获取html以get方式传过来的用户要跳转的页数的值
    if request.GET.get('num'):
        num = request.GET.get('num')
    else:
        num = 1
    # 接收一级分类id
    category = request.GET.get('category')
    # 接收二级分类id
    subcategory = request.GET.get('subcategory')
    # 创建一个subcategory_id_list列表来存储当前的一级分类下的所有二级分类的id
    subcategory_id_list = []
    # 从数据库查询一级分类，并从列表中取到该一级类别对象，用来在页面展示
    first_category_obj = Category.objects.filter(id=category)[0]
    # 根据得到的一级分类参数从数据库中查询该一级分类下的所有二级分类，用于该页面展示
    subcategory_list = Category.objects.filter(parent_id=category)
    # 如果二级类别存在，则说明用户点击的是二级分类；
    if subcategory:
        # 从数据库查询二级分类，并从列表中取到该二级类别对象，用来在页面展示
        second_category_obj = Category.objects.filter(id=subcategory)[0]
        # 上面的到的结果是字符串，需要转成int型
        current_book_category = int(subcategory)
        # 从图书表中查询该二级分类的所有图书将
        if query == "2":
            book_list = Book.objects.filter(book_category=subcategory).order_by("-sales")
        elif query =="3":
            book_list = Book.objects.filter(book_category=subcategory).order_by("book_dprice")
        elif query =="4":
            book_list = Book.objects.filter(book_category=subcategory).order_by("-publication_time")
        else:
            query = ""
            book_list = Book.objects.filter(book_category=subcategory)
    # 如果用户点击的是一级分类
    else:
        second_category_obj = 0
        current_book_category = 0
        # 遍历该一级分类下的所有二级分类，得到他们的id；用于查询相应类别下的图书；
        for ele in subcategory_list:
            # 将所有的二级分类的id追加到列表subcategory_id_list中
            subcategory_id_list.append(ele.id)
        # 根据列表subcategory_id_list中的二级类别id作为从图书表查询图书的条件
        if query == "2":
            book_list = Book.objects.filter(book_category__in=subcategory_id_list).order_by("-sales")
        elif query =="3":
            book_list = Book.objects.filter(book_category__in=subcategory_id_list).order_by("book_dprice")
        elif query =="4":
            book_list = Book.objects.filter(book_category__in=subcategory_id_list).order_by("-publication_time")
        else:
            query = ""
            book_list = Book.objects.filter(book_category__in=subcategory_id_list)

    # 将获取的图书列表进行分页，每一页5个
    page = Paginator(object_list=book_list, per_page=5).page(num)

    return render(request, 'book_category/booklist.html', {'book_list': book_list, 'subcategory_list': subcategory_list,
                                                           'first_category_obj': first_category_obj,
                                                           'current_book_category': current_book_category,
                                                           'second_category_obj': second_category_obj, 'page': page,
                                                           'user_name': user_name,"query": query})


# 跳转图书详情页面view，/dangdang/book/information/,dangdang:information
def book_information(request):
    user_name = request.GET.get("user_name")

    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session is None:
        user_name = ""

    # 接收二级分类id
    if request.GET.get('subcategory'):
        subcategory = request.GET.get('subcategory')
        subcategory = Category.objects.filter(id=subcategory)[0]
    else:
        subcategory = ''
    # 接收一级分类id
    category = request.GET.get('category')
    if category:
        category = Category.objects.filter(id=category)[0]
    else:
        category = Category.objects.filter(id=subcategory.parent_id)[0]
    # 接受书籍id
    book_id = request.GET.get('book_id')
    # 根据书籍id从书籍表中查询书籍的详细信息
    book = Book.objects.filter(book_id=book_id)[0]
    return render(request, 'book_information/Book details.html',
                  {'first_category': category, 'second_category': subcategory, 'book': book, 'user_name': user_name})
