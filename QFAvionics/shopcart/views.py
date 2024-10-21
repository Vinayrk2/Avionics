from django.shortcuts import render, redirect
from product.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.conf import settings

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    print(cart.cart)
    messages.add_message(request, messages.INFO, "Product added Successfully.")
    return redirect("/product/view/{}/".format(product.id))


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    try:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        for value in cart.cart.values():
            if value["product_id"] == id:
                if value["quantity"] == 1:
                    cart.remove(product=product)
                    return redirect("cart_detail")
                else:
                    break
        cart.decrement(product=product)
    except Exception as e:
        print(e)
    return redirect("cart_detail")

@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    total = 0
    for key,item in request.session.get("cart").items():
        total += float(item["price"]) * float(item["quantity"])
    
    shipping_charge = round(settings.CHARGES["shipping"],2)
    tax = round(settings.CHARGES["tax"]*total,2)
    print(tax)
    
    context = {
        "total": round(total+tax+shipping_charge,2),
        "sub_total": round(total,2),
        "tax": tax,
        "shipping_charge":shipping_charge
    }
    
    return render(request, 'cart_details.html',context)
