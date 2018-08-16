# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import HttpResponse, JsonResponse

# 注册
def register(request):
    return render(request, 'df_user/register.html')

# 处理注册
def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    uemail = post.get('email')
    upwd2 = post.get('cpwd')
    # 判断两次密码是否相等
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转登陆页
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET['u1']
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    return render(request, 'df_user/login.html')


def login_handle(request):
    # 获取输入
    post = request.POST
    uname = post.get('username')
    pwd = post.get('pwd')
    # 加密
    s1 = sha1()
    s1.update(pwd)
    pwd1 = s1.hexdigest()
    # user = UserInfo()
    users = UserInfo.objects.filter(uname=uname)
    # 用户名正确
    if len(users)==1:


        if users[0].name == uname:
        # pwd = users[0].upwd
        # 匹配数据库

            print('yes')
            return redirect('/user/user_center_info.html')
        print(users)
        print('no')
        return redirect('/user/login/')

    # 用户名错误
    # else:
    #     context = {
    #         'title': '用户登录', 'error_name': 1, 'error_password': 0, 'error_email': 0, 'uname': 'uname'
    #     }
    # return Http



























































