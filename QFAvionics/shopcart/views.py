from django.shortcuts import render, redirect
from product.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.filter(id=id).first()
    if product:
        cart.add(product=product)
        messages.add_message(request, messages.INFO, "Product added Successfully.")
        return redirect("/product/view/{}/".format(product.id))
    else:
        messages.add_message(request,  messages.ERROR, "Product not found.")
        return redirect("/")

@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.filter(id=id).first()
    if product:
        cart.remove(product)
        messages.add_message(request, messages.INFO, "Product Removed Successfully.")
        return redirect("cart_detail")
    else:
        messages.add_message(request,  messages.ERROR, "Product may not be available.")
        return redirect("/")

@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.filter(id=id).first()
    if product:
        cart.add(product=product)
        return redirect("cart_detail")
    else:
        messages.add_message(request,  messages.ERROR, "Product may not be available.")
        return redirect("/")

@login_required(login_url="/login/")
def item_decrement(request, id):
    try:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        
        if product:
            for value in cart.cart.values():
                if value["product_id"] == id:
                    if value["quantity"] == 1:
                        cart.remove(product=product)
                        return redirect("cart_detail")
                    else:
                        break
            cart.decrement(product=product)
        else:
            messages.add_message(request,  messages.ERROR, "Product may not be available.")
            return redirect("/")
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
    
    products = []
    for key,item in request.session.get("cart").items():
        product = Product.objects.get(pk=item["product_id"])
        item["price"] = product.price
        if request.session.get("currency") == "USD":
            item["price"] = round(float(item["price"]) * float(settings.CURRENCY_EXCHANGE_RATE),2)
        total += float(item["price"]) * float(item["quantity"])
        product = product.to_dict(request)
        product["quantity"] = item["quantity"]
        products.append(product)
    shipping_charge = round(settings.CHARGES["shipping"],2)
    tax = round(float(settings.CHARGES["tax"])*float(total),2)
    
    context = {
        "total": round(total+tax+shipping_charge,2),
        "sub_total": round(total,2),
        "tax": tax,
        "shipping_charge":shipping_charge,
        "products":products
    }
    
    return render(request, 'cart_details.html',context)

@login_required(login_url="/login/")
def send_mail_page(request):
    context = {}

    if request.method == 'POST':
        user = request.user
        cart = Cart(request)
        products = cart.cart    
        
        total = 0
        tax = float(settings.CHARGES["tax"])
        for key,item in request.session.get("cart").items():
            if request.session.get("currency") == "USD":
                item["price"] = round(float(item["price"]) * float(settings.CURRENCY_EXCHANGE_RATE),2)
            total += float(item["price"]) * float(item["quantity"])
        order_summary = {
            "total": round(float(total)+float(tax),2),
            "subtotal": round(float(total),2),
            "tax": float(tax)
        }
        subject = "Order Details"
        message = "Thank you for your order! we will contact you ASAP."  # Fallback plain text message
        html_message = render_to_string('emailtemplate.html', {
            'user': user,
            'products': products,
            'order': order_summary,
            'currency':  request.session.get("currency")
        })
        
        flag = send_mail(
            subject=subject,
            message=message,  # This is the plain text version for email clients that can't display HTML
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email, settings.EMAIL_HOST_USER],
            html_message=html_message,  # The actual HTML content
            fail_silently=False,
        )
        if flag:
            cart.clear()
        else:
            messages.add_message(request,  messages.ERROR, 'Failed to send mail, try again later')
            return redirect('/cart/cart_detail/')
        
    else:
        messages.add_message(request,  messages.INFO, 'Invalid Operation')
        return redirect("/")

    return render(request, "emailsuccess.html", {})

def get_total_items(request):
    cart = Cart(request)
    cartitems = cart.cart
    total = 0
    
    for key, value in cartitems.items():
        total += value["quantity"]    
    
    return total