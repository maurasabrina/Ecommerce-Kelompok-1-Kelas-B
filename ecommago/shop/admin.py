from django.contrib import admin
from .models import Kategori, Product, UserProfile, Cart, CartItem, Order, OrderItem

admin.site.register(Kategori)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
