from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('main/',views.main,name="main"),
    path('about/',views.about,name="about"),
    path('index/',views.index,name="index"),
    path('product/',views.product,name="product"),
    path('testimonial/',views.testimonial,name="testimonial"),
    path('why/',views.why,name="why"),
    path('cart/',views.cart,name="cart"),
    path('update_item/',views.updateItem,name="update_item"),
    path('checkout/',views.checkout,name="checkout"),
    path('process_order/',views.process_order,name="process_order"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    # path('index2/',views.index2,name="index2"),
    path('logout/',views.logout,name="logout"),
    path('detail_product/<int:pk>/',views.detail_product,name="detail_product"),
]