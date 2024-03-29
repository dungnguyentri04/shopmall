from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
#mark_safe là một hàm được sử dụng để đánh dấu một chuỗi (string) như là an toàn để hiển thị trong một trang web
# from shortuuid.django_fields import ShortUUIDField
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2,default="1.99")
    image = models.ImageField(null=True,blank=True)
    product_type = models.CharField(max_length=25,null = True)
    description = models.TextField(null=True,blank=True,default="this is a product")
    old_price = models.DecimalField(max_digits=7,decimal_places=2,default="2.99")
    brand = models.CharField(max_length=100,null=True,blank=True)
    material = models.CharField(max_length=100,null=True,blank=True)
    # colors = models.ManyToManyField('Color', through='ProductColor')# tham số through='ProductColor' trong trường ManyToManyField được sử dụng để chỉ định mô hình trung gian được sử dụng để quản lý mối quan hệ nhiều-nhiều giữa Product và Color. Trong trường hợp này, mô hình trung gian đó là ProductColor.
    specifications = models.TextField(null=True,blank=True)
    orders_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    
    def display_image(self):
        if self.imageURL is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.imageURL))
        else:
            return ""
    display_image.short_description = 'Image'
    
    @property
    def link_product(self):
        pass

    def get_precentage(self):
        new_price = (self.price/self.old_price) * 100
        return new_price
    
    def increase_orders_count(self):
        self.orders_count += 1
        self.save()  # Lưu thay đổi vào cơ sở dữ liệu
        
        

class Varient(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="varient")
    size = models.CharField(max_length=100)
    colors = models.CharField(max_length=100)
    stock_count = models.IntegerField(null=True,blank=True,default=10)

    def __str__(self):
        return self.product.name



class Image(models.Model):
    product = models.ForeignKey(Product, related_name='p_images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='related_product/')

    def __str__(self):
        return f"Images for {self.product.name}"
    


class Information(models.Model):
    product = models.ForeignKey(Product, related_name='p_informations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    informations = models.CharField(max_length=255)
    


class Feature(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="p_features")

    def __str__(self):
        return f"{self.name} of {self.product.name}"



class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=255,null=True)

    def __str__(self):
        return "Order " + str(self.id)
    
    @property
    def get_cart_total(self):
        orderItems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderItems])
        return total
    
    @property
    def get_cart_items(self):
        orderItems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderItems])
        return total
        
    

class OrderItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    size = models.CharField(max_length=100,null=True,blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
        


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=255,null=True)
    address_2 = models.CharField(max_length=255,null=True)
    district = models.CharField(max_length=255,null=True)
    province = models.CharField(max_length=255,null=True)
    zipcode = models.CharField(max_length=255,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.address

