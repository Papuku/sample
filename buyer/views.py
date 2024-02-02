from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import random
from django.conf import settings
from seller.models import * 
import razorpay

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def icons(request):
    return render(request ,'icons.html' )


def index(request):
    all_products=Product.objects.all()
    try:
        user_obj=Buyer.objects.get(email=request.session['email'])
        return render(request,'index.html',{'user_data':user_obj,'all_product':all_products})
    except:
        return render(request,'index.html',{'all_product':all_products})

def single(request):
    return render(request, 'single.html')

def about(request):
    return render(request,'about.html')

# def cart(request):
#     user_obj=Buyer.objects.get(email=request.session['email'])
#     cart_list=Cart.objects.filter(buyer=user_obj)

#     total_price=0
#     for i in cart_list:
#         total_price+=(i.product.price)

#     return render(request,'cart.html',{'cart_list':cart_list,'user_data':user_obj,'total_price':total_price})

def cart(request):
    s_email = (request.session).get('email')
    if not s_email:
        return render(request, 'login.html')
    user_data = Buyer.objects.get(email = s_email)
    cart_list = Cart.objects.filter(buyer = user_data)
    total_price = 0
    for i in cart_list:
        total_price += i.product.price
    total_price *= 100
    currency = 'INR'
    global amount
    amount = int(total_price) # Rs. 200
    if amount == 0:
        amount = 100 #because 100 paise barabar ek rupaiya hota hai
    
    
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['user_data'] = user_data
    context['cart_list'] = cart_list
    context['total_price'] = total_price
    context['rupee_total_price'] = total_price / 100

    return render(request, 'cart.html', context=context)


@csrf_exempt
def paymenthandler(request):

    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
                }
            global amount
            amount = amount
            try:
                razorpay_client.payment.capture(payment_id, amount)
                session_user = Buyer.objects.get(email = request.session['email'])
                c_objects_list = Cart.objects.filter(buyer = session_user)
                for i in c_objects_list:
                    MyOrder.objects.create(
                        buyer=session_user,
                        product=i.product,
                        status='panding'
                    )
                    i.delete()
                return render(request, 'paymentsuccess.html')
            except:
                return render(request, 'paymentfail.html')
           
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def contact(request):
    session_user = Buyer.objects.get(email = request.session['email'])
    c_objects_list = Cart.objects.filter(buyer = session_user)
    for i in c_objects_list:
        MyOrder.objects.create(
            buyer=session_user,
            product=i,
            status='panding'
            )
    return render(request,'contact.html')

def faqs(request):
    return render(request,'faqs.html')


        
def help(request):
    return render(request,'help.html')


def payment(request):
    return render(request,'payment.html')






def privacy(request):
    return render(request,'privacy.html')


def product(request):
    return render(request,'product.html')

def product2(request):
    return render(request,'product2.html')

def single2(request):
    return render(request, 'single2.html')

def terms(request):
    return render(request, 'terms.html')

def typography(request):
    return render(request, 'typography.html')

def add_row(request):
    Buyer.objects.create(
        first_name ='papu',
        last_name ='kumar',
        email='papu@gmail.com',
        password='1234567'

    )
    return HttpResponse('row added')

def register(request):
    if request.method == 'POST':
        try:
            Buyer.objects.get(email = request.POST['email'])
            return render(request,'register.html',{'msg':'email is already exists'})
        except ObjectDoesNotExist:
            if request.POST['password'] == request.POST['repassword']:
                global s_otp
                global dict_for_otp
                dict_for_otp={
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'email': request.POST['email'],
                    'password': request.POST['password']
                    }
                s_otp=random.randint(100000,999999)
                subject='for ecommerce register'
                massage=f"Hello {request.POST['first_name']},\n your otp is {s_otp}"
                from_email=settings.EMAIL_HOST_USER
                r_email=[request.POST['email']]
                send_mail(subject,massage,from_email,r_email)
                return render(request,'otp.html',{'msg':'otp has been sent to your email'})
    else:
        return render(request,'register.html')






def otp(request):
    if int(s_otp) == int(request.POST['otp']):
            Buyer.objects.create(
                first_name =dict_for_otp['first_name'],
                last_name=dict_for_otp['last_name'],
                email=dict_for_otp['email'],
                password=dict_for_otp['password']
            )
            return render(request,'index.html')

    else:
        subject='for ecommerce register'
        massage=f"Hello {dict_for_otp['first_name']},\n your otp is {s_otp}"
        from_email=settings.EMAIL_HOST_USER
        r_email=[dict_for_otp['email']]
        send_mail(subject,massage,from_email,r_email)
        
        return render(request,'otp.html',{'msg':'wrong otp enter it again'})


def resend_otp(request):
    s_otp = random.randint(100000,999999)
    subject='for ecommerce register'
    massage=f"Hello {dict_for_otp['first_name']},\n your otp is {s_otp}"
    from_email=settings.EMAIL_HOST_USER
    r_email=[dict_for_otp['email']]
    send_mail(subject,massage,from_email,r_email)
    
    return render(request,'otp.html',{'msg':'check your mailbox'})
    

def login(request):
    if request.method =='POST':
        try:
            user_obj = Buyer.objects.get(email=request.POST['email'])
            if user_obj.password == request.POST['password']:
                request.session['email']=user_obj.email
                return redirect('index')
            else:
                return render(request,'login.html',{'msg':'password is wrong'})
        except:
            return render(request,'login.html',{'msg':'email does not exists'})
    else:
        try:
            request.session['email']
            return redirect('index')
        except:
            return render(request,'login.html')



def forget(requeste):
    if requeste.method=='POST':
        try:
            user_obj=Buyer.objects.get(email=requeste.POST['email'])
            s_name=user_obj.first_name
            s_password=user_obj.password
            subject='forget password'
            massage=f'hy {s_name} your password is {s_password}'
            f_email=settings.EMAIL_HOST_USER
            r_email=[requeste.POST['email']]
            send_mail(subject,massage,f_email,r_email)
            return render(requeste,'login.html')


        except:
            return render(requeste,'foget.html',{'msg':'email does not exists'})

    else:
        return render(requeste,'forget.html')


def logout(requeste):
    del requeste.session['email']
    return redirect('index')


def edit_profile(request):
    if request.method=='GET':
        try:
            user_obj=Buyer.objects.get(email=request.session['email'])
            return render(request,'edit_profile.html',{'user_data':user_obj})
        except:
            return render(request,'login.html')
    else:
        user_row=Buyer.objects.get(email=request.session['email'])
        user_row.first_name=request.POST['first_name']
        user_row.last_name=request.POST['last_name']
        user_row.addres=request.POST['address']
        user_row.mobile=request.POST['mobile']
        user_row.pic=request.FILES['img']
        
        user_row.save()

        user_data=Buyer.objects.get(email=request.session['email'])
        return render(request,'edit_profile.html',{'user_data':user_data})
        # return render(request,'edit_profile.html')

def change_password(request):
    user_obj=Buyer.objects.get(email=request.session['email'])
    if request.method=='POST':
        if user_obj.password==request.POST['o_password']:
            if request.POST['n_password']==request.POST['cn_password']:
                user_obj.password=request.POST['n_password']
                user_obj.save()
                return render(request,'index.html',{'user_data':user_obj})
            else:
                return render(request,'change_password.html',{'msg':'please match your password','user_data':user_obj})
        
        

        else:
            return render(request,'change_password.html',{'msg':'password is wrong','user_data':user_obj})
    else:
        return render(request,'change_password.html',{'user_data':user_obj})        




def add_to_cart(request,pk):
    try:
        user_obj=Buyer.objects.get(email=request.session['email'])
        product_obj=Product.objects.get(id=pk)
        Cart.objects.create(
        buyer=user_obj,
        product=product_obj
        )
        return redirect('index')
    except:
        return render(request,'login.httml')