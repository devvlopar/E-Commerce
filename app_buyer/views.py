import email
from random import randrange
import re
from tokenize import single_quoted
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail


from app_buyer.models import Cart, User
from app_seller.models import Products
from . import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(email = request.POST['email'])
            return render(request, 'register.html',{'msg':'Email is Already Registered!!'})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global temp
                temp = {
                    'fullname': request.POST['fname'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                }

                global otp
                otp = randrange(1000,9999)
                subject = 'Welcome to Ecommerce'
                message = f'Thank you for registering and your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )

                return render(request, 'otp.html')


                # User.objects.create(
                #     fullname = request.POST['fname'],
                #     email = request.POST['email'],
                #     password = request.POST['password']
                # )
                # return render(request, 'register.html',{'msg':'Successfully Registered!! '})
            else:
                return render(request, 'register.html',{'msg':'Both passwords are not same!! '})
    else:
        return render(request, 'register.html')



def otp(request):
    if request.method == 'POST':
        if request.POST['otp'] == otp:
            User.objects.create(
                fullname = temp['fullname'],
                email = temp['email'],
                password = temp['password']
            )
            del temp
            return render(request, 'login.html', {'msg': 'Successfully Registered!!'})
    else:
        return render(request, 'otp.html')

    
def login(request):
    try:
        request.session['email']
        session_user_data = User.objects.get(email = request.session['email'])
        return render(request,'index.html',{'user_data':session_user_data})
    except:
        if request.method == 'POST':
            try:
                uid = User.objects.get(email = request.POST['email'])
                if request.POST['password'] ==  uid.password:
                    request.session['email'] = request.POST['email']
                    session_user = User.objects.get(email = request.session['email'])
                    cart_obj = Cart.objects.filter(userid = session_user)
                    global order_id
                    if len(cart_obj) != 0:
                        oid = cart_obj.values()
                        order_id = oid[0]['orderid']
                    else:
                        order_id = randrange(1000,9999)
                    return render(request, 'index.html',{'user_data':session_user})
                else:
                    return render(request, 'login.html',{'msg':'Password Incorrect!!'})
            except:
                return render(request, 'login.html', {'msg':'Email is not Registered!!'})
    return render(request, 'login.html')
   


def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def arrival(request):
    all_products = Products.objects.all()
    return render(request, 'arrivals.html',{'all_products':all_products})


def buyer_profile(request):
    if request.method == 'POST':
        session_user = User.objects.get(email = request.session['email'])
        session_user.fullname = request.POST['fname']
        session_user.password = request.POST['password']
        session_user.save()
        return render(request, 'buyer_profile.html',{'session_user':session_user,'msg':'updated!!!'})
    session_user = User.objects.get(email = request.session['email'])
    return render(request, 'buyer_profile.html',{'session_user':session_user})


def add_to_cart(request, pk):
    session_user=User.objects.get(email=request.session['email'])
    global order_id
    cart_obj = Cart.objects.filter(userid = session_user)
    if len(cart_obj) != 0:
        oid = cart_obj.values()
        order_id = oid[0]['orderid']
        pid = Products.objects.get(id=pk)
        Cart.objects.create(
            userid=session_user,
            productid=pid,
            orderid=order_id,
        )
        all_products = Products.objects.all()
        return render(request, 'arrivals.html',{'all_products':all_products})
    else:
        order_id = randrange(1000,9999)
        pid = Products.objects.get(id=pk)
        Cart.objects.create(
            userid=session_user,
            productid=pid,
            orderid=order_id,
        )
        all_products = Products.objects.all()
        return render(request, 'arrivals.html',{'all_products':all_products})


def cart(request):
    try:
        session_user=User.objects.get(email=request.session['email'])
        cart_data = Cart.objects.filter(userid = session_user, orderid=order_id)
        print(cart_data)
        return render(request, 'cart.html',{'cart_data':cart_data}) 
    except NameError:
        return redirect('login')
    except KeyError:
        return redirect('login')
    

def checkout(request):
    session_user=User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid = session_user)
    cart_data = cart_data.values()
    single_amount = 0
    for x in cart_data:
        i=0
        single_amount += x[i]['orderid']
        i+=1

    
    return render(request,'payment.html')