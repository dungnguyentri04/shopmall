import json
from .models import *


#customer not login
def cookieCart(request):
    items = []
    order = {"get_cart_items":0,"get_cart_total":0}
    cartItems = order["get_cart_items"]
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    for product_varient in cart:
        try:
            p = product_varient.split("_")
            id = p[0]
            color = p[1]
            size = p[2]
            cartItems += cart[product_varient]["quantity"]
            product = Product.objects.get(id=int(id))
            total = (product.price * cart[product_varient]["quantity"])
            order["get_cart_total"] += total
            item = {
                "product" : {
                    "id" : product.id,
                    "imageURL" : product.imageURL,
                    "name" : product.name,
                    "price" : product.price,
                },
                "quantity" : cart[product_varient]["quantity"],
                "get_total" : total,
                "color" : color,
                "size" : size,
            }
            items.append(item)
        except:
            pass
    return {"items":items,"cartItems":cartItems,"order":order}
    

def cartData(request):
    if request.user.is_authenticated:
        # print("hello3")
        # if request.user.customer:
        #     customer = request.user.customer
        # else:
            
        if hasattr(request.user, 'customer') and request.user.customer:
        # Nếu user đã có đối tượng Customer
            customer = request.user.customer
        else:
    # Nếu user chưa có đối tượng Customer, tạo mới
            customer = Customer.objects.create(user=request.user, email=request.user.email, name=request.user.username)
        # print(customer)
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData["items"]
        order = cookieData["order"]
        cartItems = cookieData["cartItems"]
    data = {'cartItems':cartItems,'order':order,'items':items}
    return data


def guessOrder(request,data):
    name = data["userFormData"]["name"]
    email = data["userFormData"]["email"]
    cookieData = cookieCart(request)
    items = cookieData["items"]
    customer,created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    order = Order.objects.create(customer = customer,complete = False)
    for item in items :
        product = Product.objects.get(id = item["product"]["id"])
        orderItem = OrderItems.objects.create(
            product = product,
            order = order,
            quantity = item["quantity"]
        )
    return customer,order