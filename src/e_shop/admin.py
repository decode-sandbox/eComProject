from django.contrib import admin

# Here are registered our models.
from .models import User, Product, Stock, Purchase

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Purchase)