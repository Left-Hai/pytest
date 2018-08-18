# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


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
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登陆', 'error_name': 0, 'error_pwd': 0, 'uname': uname
    }
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 获取输入
    post = request.POST
    uname = post.get('username')
    pwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)
    # 用户名正确
    if len(users)==1:
        # 加密
        s1 = sha1()
        s1.update(pwd)
        pwd1 = s1.hexdigest()
        # 密码正确
        if users[0].upwd == pwd1:
            red = HttpResponseRedirect('/user/user_center_info/')
            # 记住密码 ==1不行？
            if jizhu != 0:
                red.set_cookie('uname', uname)
            # 不记住密码
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        # 密码错误
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname }
            return render(request,'df_user/login.html', context)
    # 用户名错误
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'error_email': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def user_center_info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {'title': '用户中心', 'user_email': user_email,
               'user_name': request.session['user_name'], 'page_name': 1}
    return render(request, 'df_user/user_center_info.html', context)



def user_center_oeder(request):
    context = {'title': '用户中心', 'page_name': 1}
    return render(request, 'df_user/user_center_order.html', context)


def user_center_site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 如果点击提交，为post，保存数据到数据库
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)


















































