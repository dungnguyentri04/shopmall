from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)



class ProductVarientInline(admin.TabularInline):
    model = Varient
    extra = 1
    readonly_fields = ("id",)
    # classes = ('collapse', )
    can_delete = True



class ProductImageInline(admin.TabularInline):
    model = Image
    extra = 1
    classes = ("collapse",)
    can_delete = True



class ProductInformation(admin.TabularInline):
    model = Information
    extra = 1
    can_delete = True



@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["product","quantity", "display_image"]

    def display_image(self,obj):
        return obj.product.display_image()
    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVarientInline,ProductImageInline,ProductInformation]
    list_display = ["name","display_image", "price"]
    fieldsets = [
        (
            None,
            {
                "fields" : ["description","specifications"]
            }
        ),
        (
            "Base_Information",
            {
                # "classes": ["button"],: CSS type
                "fields" : ["name","material","brand","price","old_price","image","product_type"]
            }
        ),
    ]



class OrderOrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    can_delete = True
    readonly_fields = ["product","color", "size","quantity","get_total"]
    list_display = ["product","color", "size","quantity","get_total"]



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderOrderItemsInline]
    list_display = ["customer","transaction_id"]



@admin.register(ShippingAdress)
class ShippingAdressAdmin(admin.ModelAdmin):
    list_display = ["name","phone","email","order","user_display","date_added"]
    fieldsets = [
        (
            "Information",
            {
                "fields" : ["customer","name","phone","email"]
            }
        ),
        (
            "Address",
            {
                # "classes": ["button"],: CSS type
                "fields" : ["address","address_2","district","province","zipcode"]
            }
        ),
    ]

    def user_display(self,obj):
        return obj.customer.user



