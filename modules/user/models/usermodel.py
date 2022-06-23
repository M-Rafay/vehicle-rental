import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser 


from ..managers.usermanager import UserManager, UserInactiveManager,UserAllManager


class User(AbstractUser):
    # uuid = models.CharField(default=uuid.uuid4, editable=False, max_length=36)
    full_name = models.CharField(blank=True, null=True, max_length=100)
    name = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(('email address'), unique=True)
    phone_no = models.CharField(blank=True, null=True, max_length=15)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=15, default="user")
    # country = models.ForeignKey( Country, on_delete=models.CASCADE, related_name="country", blank=True,null=True)
    

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()
    inactive = UserInactiveManager()
    allusers= UserAllManager()
    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

class Customer(User):
    class Meta:
        db_table = "customers"
    
    def __str__(self):
        return self.email