from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import HomeView, ProductDetailView, ProductListView, CustomLoginView, MahsulotlarView, ProfileView, \
    SettingsView, MarketView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('product/list/<str:slug>', ProductListView.as_view(), name='product-list'),
    path('mahsulotlar', MahsulotlarView.as_view(), name='mahsulotlar'),
    path('market', MarketView.as_view(), name='market')
]

urlpatterns += [

    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('settings', SettingsView.as_view(), name='settings'),

]
