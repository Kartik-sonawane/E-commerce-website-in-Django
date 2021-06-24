from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name ='home'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('orders/', views.orders, name='orders'),

    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class= MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password-reset.html', form_class= MyPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password-reset-done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password-reset-confirm.html', form_class= MySetPasswordForm), name='password_reset_confirm'),
    path('password_change_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password-reset-complete.html'), name='password_reset_complete'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>/', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.bottomwear, name='bottomweardata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name ='app/login.html', authentication_form =LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name = 'logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
