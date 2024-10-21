from django.http import HttpResponse
from django.shortcuts import  render, redirect
import paypalrestsdk
from django.conf import settings
from cart.cart import Cart
from product.models import Product
from .models import Order


paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY
})

def create_payment(request):
    
    cart = Cart(request)
    cartitems = cart.cart
    total = sum(float(item["price"]) * float(item["quantity"]) for item in cartitems.values())
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/order/execute/",
            "cancel_url": "http://localhost:8000/order/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": item["name"],
                    "price": item["price"],
                    "currency": "CAD",
                    "sku":item["product_id"],
                    "quantity": item["quantity"]
                }
                for item in cartitems.values()
                ]
            },
            "amount": {
                "total": total,
                "currency": "CAD"
            },
            "description": "Payment For Your Order "
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                # Redirect the user to PayPal for payment approval
                return redirect(link.href)
    else:
        print(payment.error)

    return render(request, 'paypal_form.html')

# views.py

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    cart = Cart(request)
    cartitems = cart.cart
    total = sum(float(item["price"]) * float(item["quantity"]) for item in cartitems.values())
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.state == "approved":        
        return render(request, 'paypal_success.html', {"payment":payment.to_dict()})  
    if payment.execute({"payer_id": payer_id}):         
            payment_info = payment.to_dict()
            if  payment_info['state'] == 'approved' and  payment_info['payer']['payer_info']['payer_id'] == payer_id and float(payment_info["transactions"][0]["amount"]["total"]) == total and payment_info["transactions"][0]["payee"]["email"] == settings.PAYPAL_MERCHANT_EMAIL:
                product = Product.objects.get(id=int(payment_info["transactions"][0]["item_list"]["items"][0]["sku"]))
                order = Order.objects.get_or_create(user=request.user,product=product,transaction_id=payment_id,quantity=payment_info["transactions"][0]["item_list"]["items"][0]["quantity"])
                print(order[0])
                print(order[0].user)
                print(order[0].product)
                print(order[0].quantity)
                print(order[0].transaction_id)
                order[0].save()
                cart.clear()
                return render(request, 'paypal_success.html', {"payment":payment.to_dict()})
            else:
                return HttpResponse("Invalid Data")
    else:
        print(payment.error)
            # Handle payment failure
        return render(request, 'paypal_cancel.html')

def confirm_order(request):
    context = {}
    return render(request, "confirm.html", context)
