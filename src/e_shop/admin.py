from django.contrib import admin

# Here are registered our models.
from .models import User, Product, Purchase

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Purchase)