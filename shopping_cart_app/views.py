import random

import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . import cart

# Create your views here.

from home_page_app.models import Book, Address, Order, User, OrderItems


# 跳转购物车view,shopping_cart/show_ajax/,shopping_cart:show_ajax
def shopping_cart_ajax(request):
    user_name = request.GET.get("user_name")
    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session is None:
        user_name = ""
    # 从session中获取购物车对象
    my_shopping_cart = request.session.get("my_shopping_cart")
    # 接收参数book_id，和amount数量
    book_id = request.GET.get("book_id")
    amount = int(request.GET.get("amount"))
    print(type(amount), 'amount类型')
    # 根据得到的book_id来查询图书
    book = Book.objects.filter(book_id=book_id)[0]
    if my_shopping_cart is None:
        print(my_shopping_cart, 'new')
        my_shopping_cart = cart.Cart()
    my_shopping_cart = my_shopping_cart.add_books(book, amount)
    my_shopping_cart = my_shopping_cart.total_price()
    my_shopping_cart = my_shopping_cart.save_money()
    request.session["my_shopping_cart"] = my_shopping_cart
    print(my_shopping_cart.total, 'sdfsadfasdfdsafa22222222222222222')
    print(my_shopping_cart, '购物车', my_shopping_cart.total)
    print(my_shopping_cart.book_list)
    return redirect("/shopping_cart/show/?user_name=" + user_name)


# 跳转购物车view,shopping_cart/show/,shopping_cart:show
def shopping_cart(request):
    user_name = request.GET.get("user_name")
    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session is None:
        user_name = ""
    my_shopping_cart = request.session.get("my_shopping_cart")
    if (my_shopping_cart is None):
        my_shopping_cart = cart.Cart()
        request.session["my_shopping_cart"] = my_shopping_cart
    return render(request, 'shopping_cart/car.html', {"my_shopping_cart_book_list": my_shopping_cart.book_list,
                                                      "my_shopping_cart_total": my_shopping_cart.total,
                                                      'user_name': user_name,"book_list_length":len(my_shopping_cart.book_list)})


# ============测试代码========
# 清除购物车的session,shopping_cart/clear/
def clear_session(request):
    del request.session["my_shopping_cart"]
    return HttpResponse("")


# ajax处理购物车页面用户操作图书的数量,shopping_cart/change_amount/
def book_amount(request):
    # 收集图书的book_id和数量amount
    book_id = request.POST.get("book_id")
    amount = int(request.POST.get("amount"))
    print(book_id, amount)
    # 从session中得到购物车对象
    my_shopping_cart = request.session.get("my_shopping_cart")
    # 根据book_id查询book
    book = Book.objects.filter(book_id=book_id)[0]
    for i in my_shopping_cart.book_list:
        if i.book == book:
            print('ssssss', amount, i.amount)
            i.amount = amount
            print(i.amount, 'sadfsadf改变之后')
            print('ssssssssssss22222222', my_shopping_cart.book_list[0].amount, my_shopping_cart.book_list[1].amount)
            my_shopping_cart = my_shopping_cart.total_price()
            my_shopping_cart = my_shopping_cart.save_money()
            request.session["my_shopping_cart"] = my_shopping_cart
            my_shopping_cart = request.session.get("my_shopping_cart")
            print(my_shopping_cart.total, 'sdfsadfasdfdsafa')
            print(my_shopping_cart.save, "节省金额1320+855.36+360", 1320 + 855.36 + 360)
            print(my_shopping_cart.book_list)
            print(my_shopping_cart.book_list[0].amount)
            return JsonResponse({"total": my_shopping_cart.total, "save": my_shopping_cart.save})


# ajax从购物车删除书籍,shopping_cart/del_book/
def del_book_form_shoppong_cart(request):
    book_id = request.POST.get("book_id")
    book_id = book_id.split(",")
    my_shopping_cart = request.session.get("my_shopping_cart")
    print("my_shopping_cart11", my_shopping_cart)
    book = Book.objects.filter(book_id__in=book_id)
    for i in book:
        my_shopping_cart = my_shopping_cart.del_books(i)

    print("my_shopping_cart222", my_shopping_cart)
    my_shopping_cart = my_shopping_cart.total_price()
    print("my_shopping_cart13333", my_shopping_cart)
    my_shopping_cart = my_shopping_cart.save_money()
    print("my_shopping_cart1444444", my_shopping_cart)
    request.session["my_shopping_cart"] = my_shopping_cart
    my_shopping_cart_total = my_shopping_cart.total
    my_shopping_cart_save = my_shopping_cart.save
    print("==============================")
    print(my_shopping_cart.book_list)
    print(my_shopping_cart_total, my_shopping_cart_save)
    print("===================================")
    return JsonResponse(
        {"total": my_shopping_cart_total, "save": my_shopping_cart_save})


# ===========================================结算=======================
# 在购物车页面点击结算，判断登录状态，如果有用户登录，则跳转到确认订单和填写地址的页面；
# 如果没有，则跳转到用户页面。ajax。
def login_state_logic(request):
    user_name = request.POST.get("user_name")
    print(user_name, "结算测试")
    addr_id = []
    recipient_list = []
    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session is None:
        user_name = ""
    else:
        user_id = request.session.get(user_name + "_id")
        user_address_list = Address.objects.filter(addr_user_id=user_id)
        for i in user_address_list:
            addr_id.append(i.address_id)
            recipient_list.append(i.recipient_name)
    print("login_flag", user_name)
    return JsonResponse({"user_name": user_name, "addr_id": addr_id, "recipient_list": recipient_list})


# 用户确认订单，填写地址之后，跳转到订单成功页面
def indent_ok(request):
    return render(request, 'shopping_cart/indent ok.html')


def address_query(request):
    address_id = request.POST.get("address_id")
    address = Address.objects.filter(address_id=address_id)[0]
    recipient_name = address.recipient_name
    postcode = address.postcode
    tel = address.tel
    addr_mobil = address.addr_monil
    recipient_address = address.recipient_address.split("，")
    print("地址", recipient_address)
    return JsonResponse(
        {"recipient_name": recipient_name, "postcode": postcode, "addr_tel": tel, "addr_mobil": addr_mobil,
         "recipient_address": recipient_address})


def address_save(request):
    my_shopping_cart = request.session.get("my_shopping_cart")
    recipient_name = request.POST.get("recipient_name")
    detailed_address = request.POST.get("detailed_address")
    postcode = request.POST.get("postcode")
    addr_mobile = request.POST.get("addr_mobile")
    addr_tel = request.POST.get("addr_tel")
    country = request.POST.get("country")
    province = request.POST.get("province")
    buy_books_amount_list = request.POST.getlist("buy_books_amount_list")
    buy_books_id_list = request.POST.getlist("buy_books_id_list")
    buy_books_price_list = request.POST.getlist("buy_books_price_list")
    total_price = float(request.POST.get("total_price"))
    
    buy_books_amount_list = list(map(int, buy_books_amount_list))
    buy_books_id_list = list(map(int, buy_books_id_list))
    buy_books_price_list = list(map(float, buy_books_price_list))

    user_address_id = request.POST.get("user_address_id")
    print(user_address_id,'llllllllllllllllllllllllllllllllllll')
    city = request.POST.get("city")
    recipient_address = country + "，" + province + "，" + city + "，" + detailed_address
    user_name = request.POST.get("user_name")
    user_id = int(request.session.get(user_name + "_id"))

    user_obj = User.objects.filter(user_id=user_id)[0]


    order_num = int(''.join(str(random.choice(range(10))) for _ in range(5)))
    print(recipient_name,detailed_address,postcode,addr_mobile,addr_tel,country,province,buy_books_amount_list,buy_books_id_list,buy_books_price_list,user_address_id,recipient_address)
    print(type(buy_books_amount_list),type(buy_books_id_list),type(buy_books_price_list))

    # print(user_address_id,type(user_address_id))
    if user_address_id != "新增地址":
        address_obj = Address.objects.filter(address_id=int(user_address_id))
    else:
        Address(recipient_name=recipient_name, recipient_address=recipient_address, postcode=postcode, tel=addr_tel,
                addr_monil=addr_mobile, addr_user_id=user_id).save()
        all_address = Address.objects.all()
        user_address_id = all_address[len(all_address)-1].address_id

    Order(num=order_num,create_date=datetime.datetime.now(),total_price=total_price,order_address_id=user_address_id,order_user_id=user_id,status=0).save()
    order_id = Order.objects.filter(num=int(order_num))[0].order_id

    print(recipient_address,type(recipient_address),"4444")

    books_obj = Book.objects.filter(book_id__in=buy_books_id_list)
    for i in books_obj:
        my_shopping_cart = my_shopping_cart.del_books(i)

    print("my_shopping_cart222", my_shopping_cart)
    my_shopping_cart = my_shopping_cart.total_price()
    print("my_shopping_cart13333", my_shopping_cart)
    my_shopping_cart = my_shopping_cart.save_money()
    print("my_shopping_cart1444444", my_shopping_cart)

    request.session["my_shopping_cart"] = my_shopping_cart

    for i in range(len(buy_books_id_list)):
        OrderItems(item_book_id=buy_books_id_list[i],item_order_id=order_id,item_book_amount=buy_books_amount_list[i],item_total_price=buy_books_price_list[i]).save()
    print(total_price)
    print(user_address_id)
    print(total_price,type(total_price))
    return JsonResponse({"OK": "OK","indent_num":order_num,"recipient_name":recipient_name,"total_price":total_price,"books_amount":len(buy_books_id_list)})
