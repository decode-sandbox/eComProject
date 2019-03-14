from django.db import models
from django.contrib.auth.models import User as AuthUser

# Here are our models.
class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image_link = models.ImageField()
    users = models.ManyToManyField(User, through='Purchase', 
                                      related_name='products_commanded')
    
    def __str__(self):
        return self.name
    
class Stock(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} {self.product}"
    
class Purchase(models.Model):
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField()
    is_executed = models.BooleanField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.quantity} {self.product} by {self.client} the" 
        "{self.date}, Admin execute command? {self.is_executed}"