# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from df_user import user_decorator
from models import *


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'page_name': 1,
        'title': '天天生鲜-购物车',
        'carts': carts
    }
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    # 用户uid点击购买gid商品，count个
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 查询购物车内是否已经存在该商品，有数量加一，没有则新增
    carts = CartInfo.objects.filter(user_id=uid).filter(goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count+count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 如果是ajax请求则返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data={'ok': count1}
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    try:
       cart = CartInfo.objects.get(pk=int(cart_id))
       cart.delete()
       data = {'ok': 1}
    except Exception as e:
        data = {'pk': 0}
    return JsonResponse(data)

