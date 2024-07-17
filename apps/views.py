from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
import re
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView

from apps.models import Product, Category, User


class HomeView(TemplateView):
    template_name = 'apps/home.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        paginator = Paginator(Product.objects.all(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        context['products'] = page_obj

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product_detail.html'
    context_object_name = 'product'
    super_url_kwarg = 'slug'


class ProductListView(TemplateView):
    template_name = 'apps/product_list.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['products'] = Product.objects.filter(category=category)
        else:
            context['products'] = Product.objects.all()
        return context


class MahsulotlarView(TemplateView):
    template_name = 'apps/mahsulotlar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()

        return context


class MarketView(TemplateView):
    template_name = 'apps/market.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()

        return context


class CustomLoginView(TemplateView):
    template_name = 'apps/auth/login.html'

    def post(self, request, *args, **kwargs):
        phone_number = re.sub(r'\D', '', request.POST.get('phone_number'))
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            user = User.objects.create_user(phone_number=phone_number, password=request.POST['password'])
            login(request, user)
            return redirect('home')
        else:
            user = authenticate(request, username=user.phone_number, password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('home')

            else:
                context = {
                    "messages_error": ["Invalid password"]
                }
                return render(request, template_name='apps/auth/login.html', context=context)


class ProfileView(TemplateView):
    template_name = 'apps/auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()

        return context


class SettingsView(TemplateView):
    template_name = 'apps/auth/settings.html'
