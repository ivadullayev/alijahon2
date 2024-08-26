import re

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView

from apps.forms import StreamForm
from apps.models import Product, Category, User, Order, Stream, Wishlist
from apps.tasks import send_to_email


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


class MarketView(View):
    def get(self, request):
        category_slug = request.GET.get('category')
        if category_slug:
            products = Product.objects.filter(category__slug=category_slug)
        else:
            products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'selected_category': category_slug,
        }
        return render(request, template_name='apps/admin_page/market.html', context=context)


class ProductListView(ListView):
    model = Product
    template_name = 'apps/product_list.html'
    context_object_name = 'products'

    def queryset(self):
        category_slug = self.request.GET.get('category')
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        selected_category = self.request.GET.get('category')
        context['categories'] = categories
        context['selected_category'] = selected_category
        return context


class CustomRegisterView(TemplateView):
    template_name = 'apps/auth/register.html'

    def post(self, request, *args, **kwargs):
        phone_number = re.sub(r'\D', '', request.POST.get('phone_number'))
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            try:
                user = User.objects.create_user(phone_number=phone_number, email=email, password=password)
                send_to_email.delay("Siz Alijahon.uz saytidan ro'yxatdan o'tdingiz", email)  # noqa

                # generate_one_time_verification(self.request, user)
                # text = "<h3>An email has been sent with instructions to verify your email</h3>"
                # messages.add_message(self.request, messages.SUCCESS, text)

                login(request, user)
                return redirect('home')

                # return render(request, template_name=self.template_name)

            except ValueError as ve:
                context = {
                    "messages_error": [str(ve)]
                }
                return render(request, self.template_name, context)

            except ValidationError as e:
                context = {
                    "messages_error": [e.message]
                }
                return render(request, self.template_name, context)
        else:
            context = {
                "messages_error": ["Bu raqamdan avval ro'yxatdan o'tilgan!"]  # noqa
            }
            return render(request, template_name=self.template_name, context=context)


class LoginView(TemplateView):
    template_name = 'apps/auth/login.html'

    def post(self, request, *args, **kwargs):
        phone_number = re.sub(r'\D', '', request.POST.get('phone_number'))
        password = request.POST.get('password')
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            context = {
                'messages_error': ["Bu raqamdan ro'yxatdan o'tilmagan, ro'yxatdan o'ting!"]  # noqa
            }
            return render(request, template_name=self.template_name, context=context)
        else:
            user = authenticate(request, phone_number=phone_number, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                context = {
                    'messages_error': ["Password xato kiritildi!"]  # noqa
                }
                return render(request, template_name=self.template_name, context=context)


class CreateOrderView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'apps/product_detail.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        order = Order(
            name=request.POST['full_name'],
            phone_number=re.sub(r'\D', '', request.POST.get('phone_number')),
            quantity=int(request.POST.get('quantity', 1)),
            product=product

        )
        try:
            order.clean()
        except ValidationError as e:
            context = {
                "messages_error": [e.message],
                "product": product
            }
            return render(request, 'apps/product_detail.html', context=context)

        order.save()
        return redirect('order_success', order_id=order.id)


class OrderSuccessView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, template_name='apps/orders/order_success.html', context={'order': order})


class BuyurtmalarView(TemplateView):
    template_name = 'apps/orders/buyurtmalar.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.all()
        if order.exists():
            context['orders'] = order
        else:
            context['message'] = "Sizda buyurtmalar mavjud emas!"  # noqa
        return context


class StatsView(TemplateView):
    template_name = 'apps/admin_page/statistics.html'


class RequestsView(TemplateView):
    template_name = 'apps/admin_page/requests.html'


class PaymentView(TemplateView):
    template_name = 'apps/admin_page/payments.html'


class DiagramView(TemplateView):
    template_name = 'apps/admin_page/diagrams.html'


class CompetitionView(TemplateView):
    template_name = 'apps/admin_page/competition.html'


class ProfileView(TemplateView):
    template_name = 'apps/auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()

        return context


class SettingsView(TemplateView):
    template_name = 'apps/auth/settings.html'


class AdminPageView(TemplateView):
    template_name = 'apps/admin_page/admin_page.html'


# class VerifyEmailConfirm(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, 'Your email has been verified.')
#             return redirect('login')
#         else:
#             messages.warning(request, 'The link is invalid.')
#         # return render(request, 'user/verify_email_confirm.html')
#         return redirect('register')

class StreamFormView(LoginRequiredMixin, FormView):
    form_class = StreamForm
    template_name = 'apps/admin_page/market.html'

    def form_valid(self, form):
        print('valid', form.errors)
        if form.is_valid():
            form.save()
        return redirect('stream-list')

    def form_invalid(self, form):
        print('invalid', form.errors)
        return redirect('stream-list')


class StreamListVIew(ListView):
    queryset = Stream.objects.all()
    template_name = 'apps/admin_page/stream.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class WishListView(LoginRequiredMixin, ListView):
    queryset = Wishlist.objects.all()
    context_object_name = 'wishlists'
    template_name = 'apps/wishlist.html'

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user)
        return query
#
# class WishListView(LoginRequiredMixin,TemplateView):
#     template_name = 'apps/wishlist.html'  # noqa
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         wishlist = Wishlist.objects.filter(user=self.request.user)
#         if wishlist.exists():
#             context['wishlists'] = wishlist
#             print(context['wishlists'])
#         else:
#             context['message'] = "Sevimlilarim ro'yxati bo'sh!"  # noqa
#         return context
