from django.urls import path
from .views import *



urlpatterns = [
    path('icons/',icons , name= 'icons'),
    path('',index , name = 'index'),
    path('single/',single,name='single'),
    path('contact/',contact,name='contact'),
    path('about/',about,name='about'),
    path('cart/',cart,name='cart'),
    path('faqs/',faqs,name='faqs'),
    path('help/',help,name='help'),
    path('payment/',payment,name='payment'),
    path('privacy/',privacy,name='privacy'),
    path('product/',product,name='product'),
    path('product2/',product2,name='product2'),
    path('single2/',single2,name='single2'),
    path('terms/',terms,name='terms'),
    path('typography/',typography,name='typography'),
    path('add_row/',add_row,name='add_row'),
    path('register/',register,name='register'),
    path('otp/',otp,name='otp'),
    path('login/',login,name='login'),
    path('resend_otp/',resend_otp,name='resed_otp'),
    path('logout/',logout,name='logout'),
    path('forget/',forget,name='forget'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('change_password/',change_password,name='change_password'),
    path('add_to_cart/<int:pk>',add_to_cart,name='add_to_cart'),
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),
]