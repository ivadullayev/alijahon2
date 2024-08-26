from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model, CharField, ForeignKey, TextChoices, CASCADE, SlugField, BooleanField, FloatField, \
    IntegerField, SET_NULL
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Telefon raqamini kiriting!')
        if not email:
            raise ValueError('Emailingizni kiriting!')

        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)

        try:
            user.clean()
        except ValidationError as e:
            raise ValidationError(e.message)

        user.is_superuser = False
        user.is_staff = True
        user.save(using=self._db)

        # email = user.email
        # send_to_email.delay("Siz Alijahon.uz saytidan ro'yxatdan o'ttingiz", email) # noqa

        return user

    def create_superuser(self, phone_number, email, password, **extra_fields):
        user = self.create_user(phone_number, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
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
    email = models.EmailField(unique=True)
    district = ForeignKey('apps.District', CASCADE, related_name='users', null=True)

    # is_active = BooleanField(default=False)

    # class Meta:
    #     unique_together = [
    #         ('email', 'is_active'),
    #     ]

    def clean(self):
        super().clean()
        phone_number = self.phone_number
        email = self.email
        if len(phone_number) != 12:
            raise ValidationError("Telefon raqamini to'g'ri formatda kiriting!")  # noqa
        if User.objects.filter(email=self.email).exists():
            raise ValidationError("Bu emailga ega foydalanuvchi allaqachon mavjud!")  # noqa


class Region(Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, unique=True)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BaseModel(Model):
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

    name = models.CharField(max_length=100, verbose_name='kategoriya nomi')  # noqa
    image = models.ImageField(upload_to='images/', blank=True)

    def delete(self, using=None, keep_parents=False):
        self.image.delete(False)
        return super().delete(using, keep_parents)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/images/')
    price = models.DecimalField(max_digits=50, decimal_places=0)
    description = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    shipping_price = models.DecimalField(max_digits=50, decimal_places=0)
    payment = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    reserve = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    discount = models.CharField(default="yo'q", max_length=50)

    def get_total_price(self):
        return self.price + self.shipping_price

    def delete(self, using=None, keep_parents=False):
        self.image.delete(False)
        return super().delete(using, keep_parents)

    def __str__(self):
        return self.name


class Order(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Buyurtmachi ismi')  # noqa
    phone_number = models.CharField(max_length=12, verbose_name='buyurtmachi telefon raqami')  # noqa
    quantity = models.IntegerField(default=1, verbose_name='buyurtma soni')  # noqa
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')
    created_adt = models.DateTimeField(auto_now_add=True, verbose_name='buyurtma qilingan vaqt')  # noqa

    def clean(self):
        super().clean()
        phone_number = self.phone_number
        if len(phone_number) != 12:
            raise ValidationError("Telefon raqamini to'g'ri kiriting!")  # noqa

    def __str__(self):
        return self.name


class Specification(Model):
    key = CharField(max_length=50)
    value = CharField(max_length=255)
    product = ForeignKey('apps.Product', on_delete=models.CASCADE, related_name='specifications')

    def __str__(self):
        return self.key


class Stream(BaseModel):
    name = CharField(max_length=100)
    discount = FloatField()
    count = IntegerField(default=0)
    product = ForeignKey('apps.Product', SET_NULL, null=True, related_name='streams')
    owner = ForeignKey(User, on_delete=CASCADE, related_name='streams')

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class Wishlist(Model):
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='wishlists', to_field='slug')
    user = ForeignKey(User, on_delete=CASCADE, related_name='wishlists')

    def __str__(self):
        return self.product.name
