from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CharField, ForeignKey, TextChoices, CASCADE, SlugField
from django.utils.text import slugify


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        return user


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = "admin", 'Admin'
        OPERATOR = "operator", 'Operator'
        MANAGER = "manager", 'Manager'
        DRIVER = "driver", 'Driver'
        USER = "user", 'User'

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone_number = CharField(max_length=12, unique=True)
    district = ForeignKey('apps.District', CASCADE, related_name='users', null=True)


class Region(Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, unique=True)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    created_adt = models.DateTimeField(auto_now_add=True)
    updated_adt = models.DateTimeField(auto_now=True)
    slug = SlugField(unique=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)


class Category(BaseModel):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=50, decimal_places=0)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    shipping_price = models.DecimalField(max_digits=50, decimal_places=0)
    payment = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    reserve = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    discount = models.CharField(default="yo'q", max_length=50)


class Specification(Model):
    key = CharField(max_length=50)
    value = CharField(max_length=255)
    product = ForeignKey('apps.Product', on_delete=models.CASCADE, related_name='specifications')

    def __str__(self):
        return self.key
