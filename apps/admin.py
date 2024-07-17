from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.models import Category, Product, Specification, User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = 'name',
    exclude = ('slug',)


class SpecificationAdmin(StackedInline):
    model = Specification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SpecificationAdmin]
    exclude = ('slug',)


  

    # list_display = 'id', 'name', 'price', 'category', 'show_image'
    # autocomplete_fields = 'category',
    #
    # @admin.display(description='Image')
    # def show_image(self, obj: Product):
    #     if obj.image:
    #         return mark_safe(f'<img src="{obj.image.url}" width="60" height="50" />')
    #     else:
    #         return "rasm mavjud emas"
