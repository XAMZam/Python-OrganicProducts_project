from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, OrderItem, Customer, ShippingAddress
from django.conf import settings
import json
import datetime
import requests
from .utils import cartData, guestOrder
from requests.auth import HTTPBasicAuth

def get_safaricom_token():
    consumer_key = settings.SAFARICOM_CONSUMER_KEY
    consumer_secret = settings.SAFARICOM_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        return None

@csrf_exempt
def get_safaricom_token_view(request):
    try:
        token = get_safaricom_token()
        if token:
            return JsonResponse({'access_token': token}, status=200)
        else:
            return JsonResponse({'error': 'Failed to obtain token'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def initiate_mpesa_payment_view(request):
    try:
        data = json.loads(request.body)
        # Add logic to initiate M-Pesa payment with the provided data
        # You will need to use the token and make a request to Safaricom's API
        # Example:
        # result = initiate_mpesa_payment(data)
        # return JsonResponse(result)
        return JsonResponse({'status': 'success', 'message': 'M-Pesa payment initiated'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_cart_data(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_items = order.get_cart_items
    return items, order, cart_items

@login_required
def store(request):
    # Get cart data
    data = cartData(request)
    cart_items = data['cartItems']
    order = data['order']

    products = Product.objects.all()

    # Check if products are successfully retrieved
    if products:
        # Empty the cart if products are available
        order_items = OrderItem.objects.filter(order=order)
        order_items.delete()

    context = {'products': products, 'cartItems': cart_items, 'order': order}
    return render(request, 'store/store.html', context)

def cart(request):

    data= cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
   
   data= cartData(request)
   items = data['items']
   order = data['order']
   cart_items = data['cartItems']

   context = {'items': items, 'order': order, 'cartItems': cart_items}
   return render(request, 'store/checkout.html', context)

@login_required
def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', product_id)

    customer = request.user.customer
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was updated', safe=False)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
    try:
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            customer, order = guestOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
            order.save()

            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )

        return JsonResponse('Payment complete!', safe=False)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)