from django.http import HttpResponse
from django.shortcuts import  render, redirect
import paypalrestsdk
from django.conf import settings
from cart.cart import Cart
from product.models import Product
from .models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages


paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY
})

def create_payment(request):
    if request.method == 'GET':
        messages.error(request, 'Invalid request')
        return redirect('home')
    cart = Cart(request)
    user = request.user
    cartitems = cart.cart
    address = request.POST.get("address")
    total = sum(float(item["price"]) * float(item["quantity"]) for item in cartitems.values())
    shipping = round(settings.CHARGES["shipping"],2)
    tax = round(settings.CHARGES["tax"] * total,2)
    
    
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
                    "quantity": item["quantity"],
                    "image_url":  item["image"],
                }
                for item in cartitems.values()
                ]
            },
            "shipping_address":{
                "recipient_name": "{} {}".format(user.first_name,  user.last_name),
                "line1" : "Toronto",
                "city": "Cs-ds",
                "state": "LA",
                "postal_code": "12345",
                "country_code":"212121"
            },
            "amount": {
                "total": str(round(total + shipping + tax,2)),
                "currency": "CAD",
                "details":{
                "subtotal":str(total),
                "tax":str(tax),
                "shipping":str(shipping),
                }
                
            },
            # "description": "Payment For Your Order "
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                # Redirect the user to PayPal for payment approval
                return redirect(link.href)
    else:
        print(payment.error)
        return render(request, '500.html', {"error":payment.error})


# views.py

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    cart = Cart(request)
    cartitems = cart.cart
    user = request.user
    total = sum(float(item["price"]) * float(item["quantity"]) for item in cartitems.values())
    total = total + round(settings.CHARGES["tax"]*total,2) + round(settings.CHARGES["shipping"])
    payment = paypalrestsdk.Payment.find(payment_id)
    # print(payment)
    if payment.state == "approved":        
        payment_info = payment.to_dict()
        
        return render(request, 'paymentSuccess.html', {"payment":payment.to_dict()})  
    if payment.execute({"payer_id": payer_id}):         
            payment_info = payment.to_dict()
            if  payment_info['state'] == 'approved' and  payment_info['payer']['payer_info']['payer_id'] == payer_id and float(payment_info["transactions"][0]["amount"]["total"]) == total and payment_info["transactions"][0]["payee"]["email"] == settings.PAYPAL_MERCHANT_EMAIL:
                # product = Product.objects.get(id=int(payment_info["transactions"][0]["item_list"]["items"][0]["sku"]))
                
                products = payment_info["transactions"][0]["item_list"]["items"]
                amount = payment_info["transactions"][0]["amount"]["details"]
                status = payment_info['state']
                order_id = payment_info['cart']
                payer_id = payment_info['payer']['payer_info']['payer_id']
                address = payment_info["transactions"][0]["item_list"]["shipping_address"]
                print(products, amount,  status, order_id, payer_id, address)

                order = Order.objects.get_or_create(user=user, amount_summary=amount, transaction_id=payment_info["id"], payment_status=status, order_id=order_id, payer_id=payer_id, items={"products":products}, address=address )
                cart.clear()
                return render(request, 'paymentSuccess.html', {"payment":payment.to_dict()})
            else:
                return HttpResponse("Invalid Data")
    else:
        print(payment.error)
            # Handle payment failure
        return render(request, 'paymentCancel.html')

@login_required(login_url="/login/")
def confirm_order(request):
    total = 0
    for key,item in request.session.get("cart").items():
        total += float(item["price"]) * float(item["quantity"])

    shipping_charge = round(settings.CHARGES["shipping"],2)
    tax = settings.CHARGES["tax"]*total
    
    context = {
        "total": round(total+tax+shipping_charge,2),
        "sub_total": round(total,2),
        "tax": tax,
        "shipping_charge":shipping_charge
    }
    return render(request, "confirm.html", context)