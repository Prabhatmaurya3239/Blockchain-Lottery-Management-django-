# lottery_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)
    
class User(AbstractBaseUser):
    User_id = models.AutoField(primary_key=True)  # Optional, Django adds this by default
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    walet_address = models.CharField(max_length=42, unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)  # Automatically sets signup date
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)   
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name', 'date_of_birth', 'walet_address']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
class Lottery(models.Model):
    lottery_id = models.AutoField(primary_key=True)  
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    lottery_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    contract_address = models.CharField(max_length=42, unique=True)
    is_active = models.BooleanField(default=True)
    winner_address = models.CharField(max_length=42, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_Deployed =  models.BooleanField(default=False)
    image_field = models.ImageField(upload_to='static/lottery_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
       return self.lottery_name
class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)  
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    wallet_address = models.CharField(max_length=42)
    is_winner = models.BooleanField(default=False)
    wining_amount = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    lottery_number = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
class solidity(models.Model):
    solidity_id = models.AutoField(primary_key=True)  
    ABI = models.TextField()
    Byte_code = models.TextField()
    Code = models.TextField()
   