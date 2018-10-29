import hashlib

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random

# Create your views here.


from home_page_app.models import User

# 跳转用户登录页面的view,customer/login/page/
def login_page(request):
    shopping_cart = request.GET.get("shopping_cart")
    if shopping_cart is None:
        shopping_cart = ""
    print(shopping_cart,"登录的购物车标记")
    return render(request, 'customer/login.html',{"shopping_cart": shopping_cart})


# 跳转注册页面的view,customer/register/page/
def register_page(request):
    return render(request, 'customer/register.html')

# 跳转到注册成功页面的view,customer/register/ok/
def register_ok_page(request):
    user_mobile = request.GET.get('user_mobile')
    user_name = request.GET.get('user_name')
    print(user_mobile)
    return render(request, 'customer/register ok.html',{"user_mobile": user_mobile, "user_name": user_name})


# ajax接收注册页面用户名，并对其进行验证的view，customer/register/username_confirm/
def register_username_confirm(request):
    username = request.POST.get('username')
    print(username)
    print('shuzi?', username.isdigit())
    if len(username) != 11:
        return HttpResponse("wrong")
    elif User.objects.filter(user_mobile=username):
        return HttpResponse("used")
    elif username.isdigit() is False:
        return HttpResponse("wrong")
    elif User.objects.filter(user_mobile=username) is not None and username.isdigit():
        return HttpResponse("yes")

# ajax接受注册页面的验证码信息，并验证的view,customer/register/captcha_confirm/
def register_captcha_confirm(request):
    captcha_code_user = request.POST.get('captcha_code')
    captcha_code_real = request.session.get('code')
    print('user:', captcha_code_user, 'old: ',captcha_code_real)
    if captcha_code_user == captcha_code_real:
        return HttpResponse("yes")
    else:
        return HttpResponse("wrong")

# 处理用户注册信息的view,customer/register/logic/
def register_logic(request):
    # 接受用户的注册信息
    user_mobile = request.POST.get('user_mobile')
    captcha_code = request.POST.get('captcha_code')
    pwd = request.POST.get('pwd')
    # 创建一个随机盐的字符串库
    l = '1234567890qweiosdfghjklzxcvbnm,\./!@#$%^&*()'
    # 从随机盐库中随机取6个字符得到随机盐
    solt = ''.join(random.sample(l, 6))
    print(solt)
    # 创建哈希对象
    h = hashlib.md5()
    # 将密码与随机盐组合，得到一个新的密码
    password = pwd + solt
    # 将得到的新密码进行哈希
    h.update(password.encode())
    # 得到哈希之后的字符串
    pwd = h.hexdigest()
    user_name = "maxin"+''.join(str(random.choice(range(10))) for _ in range(3))
    print('user_mobile:',user_mobile,'captcha_code:',captcha_code,'pwd:',pwd)
    # 将得到的数据入库
    User(user_mobile=user_mobile,user_password=pwd,user_solt=solt,user_name=user_name).save()
    new_user = User.objects.filter(user_mobile=user_mobile)[0]
    request.session[user_name + "_login_state"] = user_name
    request.session[user_name + "_id"] = new_user.user_id
    return JsonResponse({"yes":"yes","user_name": user_name})

# 处理用户登录信息的view,customer/login/logic/
def login_logic(request):
    # 接收用户的登录信息参数
    user_mobile = request.POST.get('user_mobile')
    user_pwd = request.POST.get('pwd')
    # 根据接受的参数到数据库中查询User表
    user = User.objects.filter(user_mobile=user_mobile)
    # 如果不为空，则说明用户的手机号输入正确，在对用户输入的密码进行判断
    if user:
        # 得到用户的盐
        solt = user[0].user_solt
        # 得到用户的密码
        pwd1 = user[0].user_password
        # 得到用户的昵称
        user_name = user[0].user_name
        user_id= user[0].user_id
        # 创建一个哈希对象
        h = hashlib.md5()
        # 将用户输入的密码信息与取出来的盐进行拼接
        password = user_pwd + solt
        # 将拼接之后的字符串进行哈希
        h.update(password.encode())
        # 得到哈希之后的字符串
        pwd2 = h.hexdigest()
        print('用户的输入信息：',user_mobile, user_pwd)
        print('pwd1: ',pwd1, 'pwd2: ', pwd2,pwd1==pwd2)
        # 对上述哈希之后的密码与User[0].user_password进行验证,如果相等，则说明登录信息正确
        if pwd2==pwd1:
            request.session[user_name+"_login_state"] = user_name
            request.session[user_name + "_id"] = user_id
            print(request.session.get(user_name + "_login_state"),"sssssssssssssssssssssssssss")
            print(request.session.get(user_name + "_id"),"ssssssssssssssssssssssssssssss")
            return JsonResponse({"msg":"yes","user_name": user_name})
        # 如果不匹配，则说明用户的登录密码错误返回信息
        return JsonResponse({"msg":"pwd_wrong"})
    # 如果查询结果为空，则说明用户登录信息错误，返回错误信息
    else:
        return JsonResponse({"msg": "mobile_wrong"})

# 用户登出view
def log_out(request):
    user_name = request.GET.get("user_name")
    if user_name is None:
        user_name = random.choice("QWERTYUIOSDFGHJKXCVBNMSDFGHJqwertyuiopasdfghjklzxcvbnm")
    user_name_session = request.session.get(user_name + "_login_state")
    if user_name_session:
        del request.session[user_name + "_login_state"]
        del request.session[user_name + "_id"]
    else:
        user_name = ""
    return redirect("/dangdang/home/?user_name="+user_name)