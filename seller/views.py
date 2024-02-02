from django.shortcuts import render,redirect
from .models import *

from django.core.exceptions import ObjectDoesNotExist
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def seller_index(request):
    try:
        # print(request.session['seller_email'])
        seller_obj=Seller.objects.get(email=request.session['seller_email'])
        all_order=MyOrder.objects.filter(product__seller=seller_obj)
        return render(request,'seller_index.html',{'seller_data':seller_obj,'order_data':all_order})
    except:
        try:
            request.session['seller_email']
            return render(request,'seller_index.html',{'seller_data':seller_obj})
        except:
            return render(request,'signin.html')
def signup(request):
    if request.method == 'POST':
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request,'signup.html',{'msg':'email is already exists'})
        except ObjectDoesNotExist:
            if request.POST['password'] == request.POST['repassword']:
                global seller_dict_for_otp
                seller_dict_for_otp={
                    'full_name': request.POST['full_name'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                    'mobile':request.POST['mobile'],
                    'gst_no':request.POST['gst_no']
                    }
                global s_otp
                s_otp=random.randint(100000,999999)
                subject='for ecommerce register'
                massage=f"Hello {request.POST['full_name']},\n your otp is {s_otp}"
                from_email=settings.EMAIL_HOST_USER
                r_email=[request.POST['email']]
                send_mail(subject,massage,from_email,r_email)
                return render(request,'seller_otp.html',{'msg':'otp has been sent to your email'})
    else:
        return render(request,'signup.html')


def seller_otp(request):
    if int(s_otp) == int(request.POST['seller_otp']):
            Seller.objects.create(
                full_name =seller_dict_for_otp['full_name'],
                mobile_number=seller_dict_for_otp['mobile'],
                email=seller_dict_for_otp['email'],
                password=seller_dict_for_otp['password'],
                gst=seller_dict_for_otp['gst_no']
            )
            return render(request,'seller_index.html')

    else:
        return render(request,'otp.html',{'msg':'wrong otp enter it again'})

def signin(request):
    if request.method=='POST':
        try:
            seller_obj=Seller.objects.get(email=request.POST['email'])
            if seller_obj.password==request.POST['password']:
                request.session['seller_email']=request.POST['email']
                # print(request.session['seller_email'])
                return render(request,'seller_index.html',{'seller_data':seller_obj})
            else:
                return render(request,'signin.html',{'msg':'password is wrong'})
        except:
            return render(request,'signin.html',{'msg':'email does not exists'})

    return render(request,'signin.html')


def seller_edit_profile(request):
     seller_obj=Seller.objects.get(email=request.session['seller_email'])
     if request.method=='GET':
        return render(request,'seller_edit_profile.html',{'seller_data':seller_obj})
     else:
        seller_obj.full_name=request.POST['full_name']
        seller_obj.gst=request.POST['gst_no']
        seller_obj.mobile_number=request.POST['mobile']
        seller_obj.save()

       

        return render(request,'seller_edit_profile.html',{'seller_data':seller_obj})


def seller_logout(request):
    del request.session['seller_email']
    return redirect('seller_index')



def my_product(request):
    seller_obj=Seller.objects.get(email = request.session['seller_email'])
    proobj=Product.objects.filter(seller=seller_obj)

    return render(request,'my_product.html',{'seller_data':seller_obj,'product_data':proobj})



def add_product(request):
        seller_obj=Seller.objects.get(email = request.session['seller_email'])
        if request.method=='POST':
            Product.objects.create(
                product_name=request.POST['product_name'],
                dec=request.POST['des'],
                price=request.POST['price'],
                pic=request.FILES['pic'],
                seller=seller_obj

            )
            return render(request,'seller_index.html',{'seller_data':seller_obj})
        else:
            return render(request,'add_product.html',{'seller_data':seller_obj})
 
def edit_product(request,pk):
    seller_obj=Seller.objects.get(email=request.session['seller_email'])
    pro_obj=Product.objects.get(id = pk)
    if request.method== 'GET':
        return render(request,'edit_product.html',{'seller_data':seller_obj,'product_data':pro_obj})
    else:
        pro_obj.product_name=request.POST['product_name']
        pro_obj.dec=request.POST['dec']
        pro_obj.price=request.POST['price']
        pro_obj.pic=request.FILES['pic']
        pro_obj.save()
        return render(request,'edit_product.html',{'seller_data':seller_obj,'product_data':pro_obj})

def delete_product(request,pk):
    seller_obj=Seller.objects.get(email=request.session['seller_email'])
    pro_obj=Product.objects.get(id =pk)
    pro_obj.delete()
    return redirect('my_product')


def form(request):
    return render(request,'form.html')

def table(request):
    return render(request,'table.html')


def my_order(request):
    return(request,'my_order.html')
    

def change_status(request,pk):
    order_obj=MyOrder.objects.get(id=pk)
    order_obj.status='dispatched'
    order_obj.save()

    return redirect('seller_index')
