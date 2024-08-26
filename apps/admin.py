from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin import StackedInline
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.models import Category, Product, Specification, User, Order, Wishlist

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    search_fields = 'name',
    exclude = ('slug',)

    list_display = ('name', 'show_image')

    @admin.display(description='kategoriya rasmi')
    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="50" />')
        else:
            return "rasm mavjud emas"


class SpecificationAdmin(StackedInline):
    model = Specification


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    exclude = ('slug',)
    list_display = ('name', 'phone_number', 'quantity', 'created_adt', 'show_image')
    search_fields = ['name']

    @admin.display(description='mahsulot rasmi')
    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.product.image.url}" width="50% height="40">')


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [SpecificationAdmin]
    exclude = ('slug',)
    search_fields = ['name']

    list_display = 'id', 'name', 'price', 'category', 'show_image'
    autocomplete_fields = 'category',

    @admin.display(description='Image')
    def show_image(self, obj: Product):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="50" />')
        else:
            return "rasm mavjud emas"


@admin.register(Wishlist)
class WishlistAdmin(ModelAdmin):
    exclude = 'slug',
