from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import HomeView, ProductDetailView, ProductListView, ProfileView, \
    SettingsView, MarketView, CreateOrderView, OrderSuccessView, BuyurtmalarView, \
    StatsView, RequestsView, PaymentView, DiagramView, CompetitionView, AdminPageView, LoginView, \
    CustomRegisterView, StreamFormView, StreamListVIew, WishListView

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('market/', MarketView.as_view(), name='market'),
]

urlpatterns += [

    path('register', CustomRegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('login', LoginView.as_view(), name='login'),

    path('profile', ProfileView.as_view(), name='profile'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('admin-page', AdminPageView.as_view(), name='admin_page'),

]

urlpatterns += [
    path('order/create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
    path('order/success/<int:order_id>', OrderSuccessView.as_view(), name='order_success'),
    path('buyurtmalar/', BuyurtmalarView.as_view(), name='buyurtmalar'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
]

urlpatterns += [
    path('stats/', StatsView.as_view(), name='stats'),
    path('requests/', RequestsView.as_view(), name='request'),
    path('payments/', PaymentView.as_view(), name='payment'),
    path('diagrams/', DiagramView.as_view(), name='diagrams'),
    path('competition/', CompetitionView.as_view(), name='competition'),
    path('stream/form', StreamFormView.as_view(), name='stream-form'),
    path('stream/list', StreamListVIew.as_view(), name='stream-list'),
]

#
# urlpatterns += [
#
#         path('verify-email-confirm/<uidb64>/<token>/', VerifyEmailConfirm.as_view(), name='verify-email-confirm'),
# ]
