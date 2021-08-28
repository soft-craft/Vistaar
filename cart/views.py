from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Products
from .cart import Cart
from .forms import CartAddProductForm
from account.models import Profile


@require_POST
def cart_add(request, products_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=products_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(products=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, products_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=products_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        current_user = request.user
        user_profile = Profile.objects.filter(user=current_user).first()
    else:
        user_profile = 0
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'cart/detail.html', {'cart': cart,'user_profile':user_profile})