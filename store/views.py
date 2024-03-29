from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guessOrder
from django.contrib import auth,messages
from django.urls import reverse,resolve
import random


# Templete main
def main(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    context = {"cartItems":cartItems}
    return render(request,"store/main.html",context)


# Templete about
def about(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    context = {"cartItems":cartItems}
    return render(request,"store/about.html",context)


# Templete index
def index(request):    
    data = cartData(request)
    cartItems = data["cartItems"]
    context = {"cartItems":cartItems}
    return render(request,"store/index.html",context)


# Templete product
def product(request):
    products = Product.objects.all()
    data = cartData(request)
    cartItems = data["cartItems"]
    context = {"products":products,"cartItems":cartItems}
    return render(request,"store/product.html",context)


# Templete testimonial
def testimonial(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    context = {"cartItems":cartItems}
    return render(request,"store/testimonial.html",context)


# Templete why
def why(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    context = {"cartItems":cartItems}
    return render(request,"store/why.html",context)
    

# Templete cart
def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    context = {"items":items,"order":order,"cartItems":cartItems}
    return render(request,"store/cart.html",context)


# Add,Remove,Delete Item
def updateItem(request):
    # print("rwff")
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    quantity = data["quantity"]
    color = data["varient"]["color"]
    size = data["varient"]["size"]
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer = customer,complete=False)
    orderItem,created = OrderItems.objects.get_or_create(order = order,product = product,color = color,size =size)
    if action == "add":
        orderItem.quantity += quantity
    elif action == "remove":
        orderItem.quantity -= 1
    elif action == "delete":
        orderItem.quantity = 0
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("",safe=False)


    
#checkout
def checkout(request):
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]
    context = {"items" : items,"order": order,"cartItems":cartItems}
    return render(request,"store/checkout.html",context)


#processOrder
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
    else:
        # note***
        customer,order = guessOrder(request,data)
    total = float(data["userFormData"]["total"])
    order.transaction_id = transaction_id
    if float(order.get_cart_total) == total:
        order.complete = True
    order.save()
    ShippingAdress.objects.create(
        customer = customer,
        order = order,
        address = data["shippingInfo"]["address"],
        address_2 = data["shippingInfo"]["address_2"],
        province = data["shippingInfo"]["province"],
        district = data["shippingInfo"]["district"],
        zipcode = data["shippingInfo"]["zipcode"],
        name = data["userFormData"]["name"],
        email = data["userFormData"]["email"],
        phone = data["userFormData"]["phone"],
        date_added = datetime.datetime.now().date()
    )
    return JsonResponse("",safe=False)


#register
def register(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    context = {"items":items,"order":order,"cartItems":cartItems}
    if request.method == "POST":
        username = request.POST['fullname']
        password =  request.POST['password']
        email = request.POST['email']
        password_confirm = request.POST['password_confirm']
        if password == password_confirm:
            if User.objects.filter(email = email).exists():
                messages.success(request,("The email is exist"))
                return redirect("register")
            elif User.objects.filter(username = username).exists():
                messages.success(request,("Username is exist"))
                return redirect("register")
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect("login")
        else:
            messages.success(request,("Password not the same"))
            return redirect("register")
    else:
        return render(request,"store/register.html",context)
    

    #login
def login(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    context = {"items":items,"order":order,"cartItems":cartItems}
    if request.method == "POST":
        username = request.POST.get("fullname")
        password = request.POST.get("password")
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else: 
            messages.success(request,("The account is not exist"))
            return redirect("login")
    else:
        return render(request,"store/login.html",context)
    

# Templete index
# def index2(request):    
#     data = cartData(request)
#     cartItems = data["cartItems"]
#     context = {"cartItems":cartItems}
#     return render(request,"store/index2.html",context)


# logout
def logout(request):
    auth.logout(request)
    return redirect('main')


#draft
def detail_product(request,pk):
    product = Product.objects.get(id = pk)
    #random 4 products related
    related_products = Product.objects.filter(product_type = product.product_type).exclude(id=pk)
    related_products = list(related_products)
    if len(related_products) > 4:
        random.shuffle(related_products)
        related_products =related_products[:4]
    data = cartData(request)
    cartItems = data["cartItems"]
    p_images = product.p_images.all()
    varients = product.varient.all()
    informations = product.p_informations.all()
    if informations.exists():
        pass
    else:
        informations = ""
    if varients.exists():
        colors = [varient.colors for varient in varients]
        colors = set(colors)
        sizes = [varient.size for varient in varients]
        sizes = set(sizes)
    else:
        colors = ""
        sizes = ""
    
    context = {
        "cartItems":cartItems,
        "product":product,
        "p_images":p_images,
        "related_products":related_products,
        "colors":colors,
        "sizes":sizes,
        "informations":informations,
        }
    return render(request,"store/detail_product.html",context)