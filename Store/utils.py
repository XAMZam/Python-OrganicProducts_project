import json
from .models import Product,Order,Customer,OrderItem

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except:
        cart = {}
    
    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for i in cart:
        try:
            cart_items += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL,
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)

            if not product.digital:
                order['shipping'] = True
        except Product.DoesNotExist:
            pass

    return {'order': order, 'cartItems': cart_items, 'items': items}


def cartData(request):
     
     if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
     else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cart_items = cookieData['cartItems']
     return{'order': order, 'cartItems': cart_items, 'items': items}

def guestOrder(request, data):
    print('User is not logged in.')
    print('COOKIE:', request.COOKIES)
    
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    
    return customer, order