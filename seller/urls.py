from django.urls import path
from .views import *



urlpatterns=[
    path('signin/',signin,name='signin'),
    path('signup/',signup,name='signup'),
    path('seller_index/',seller_index,name='seller_index'),
    path('form/',form,name='form'),
    path('table/',table,name='table'),
    path('seller_otp/',seller_otp,name='seller_otp'),
    path('',seller_index,name='seller_index'),
    path('seller_edit_profile/',seller_edit_profile,name='seller_edit_profile'),
    path('seller_logout/',seller_logout,name='seller_logout'),
    path('my_product/',my_product,name='my_product'),
    path('add_product/',add_product,name='add_product'),
    path('edit_product/<int:pk>',edit_product,name='edit_product'),
    path('delete_product/<int:pk>',delete_product,name='delete_product'),
    path('my_order/',my_order,name='my_order'),
    path('change_status/<int:pk>',change_status,name='change_status')
]