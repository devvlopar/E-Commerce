import email
from random import randrange
import re
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail


from app_buyer.models import User
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
                    session_user_data = User.objects.get(email = request.session['email'])
                    return render(request, 'index.html',{'user_data':session_user_data})
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
