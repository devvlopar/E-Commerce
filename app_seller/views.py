from random import randrange
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail


from app_seller.models import *


# Create your views here.
def add_product(request):
    if request.method == 'POST':
        pass
    return render(request, 'addproduct.html')

def seller_register(request):
    if request.method == 'POST':
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request, 'sellerregister.html',{'msg':'Email is Already Registered!!'})
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

                return render(request, 'sellerotp.html')
            else:
                return render(request, 'sellerregister.html',{'msg':'Both passwords are not same!! '})
    else:
        return render(request, 'sellerregister.html')


def seller_otp(request):
    if request.method == 'POST':
        uotp = int(request.POST['otp'])
        if uotp == otp:
            Seller.objects.create(
                fullname = temp['fullname'],
                email = temp['email'],
                password = temp['password']
            )
            
            return render(request, 'sellerlogin.html', {'msg': 'Successfully Registered!!'})
        return render(request, 'sellerotp.html', {'msg': 'OTP is wrong!!'})
        
    else:
        return render(request, 'sellerotp.html')

    
def seller_login(request):
    try:
        request.session['email']
        session_user_data = Seller.objects.get(email = request.session['email'])
        return render(request,'addproduct.html',{'user_data':session_user_data})
    except:
        if request.method == 'POST':
            try:
                uid = Seller.objects.get(email = request.POST['email'])
                if request.POST['password'] ==  uid.password:
                    request.session['email'] = request.POST['email']
                    session_user_data = Seller.objects.get(email = request.session['email'])
                    return render(request, 'addproduct.html',{'user_data':session_user_data})
                else:
                    return render(request, 'sellerlogin.html',{'msg':'Password Incorrect!!'})
            except:
                return render(request, 'sellerlogin.html', {'msg':'Email is not Registered!!'})
    return render(request, 'sellerlogin.html')
   


def seller_logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'sellerlogin.html')
    except:
        return render(request, 'sellerlogin.html')

def arrival(request):

    return render(request, 'arrivals.html')