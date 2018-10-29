import os
import random
import string

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from captcha_app.captcha133.image import ImageCaptcha

# 生成验证码图片view，captcha/show/captcha/
def get_captcha(request):
    """
    生成验证码，响应给浏览器
    1.随机码（字符串）
    2.把码转成图片
    3.响应给浏览器
    :param request:
    :return:
    """
    # 1.创建一个ImageCaptcha对象
    cap = ImageCaptcha(fonts=[os.path.abspath("captcha133/font/segoesc.ttf")])
    # 2.获取5为长度，随机验证码值
    code_list = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5)
    code = "".join(code_list)
    # 3.将验证码存入session
    request.session["code"] = code
    print("验证码是：", code)
    # 4.生成验证码图片（核心）
    data = cap.generate(code)
    # 5.写出图片"image/png"是png的类型格式
    return HttpResponse(data, "image/png")

