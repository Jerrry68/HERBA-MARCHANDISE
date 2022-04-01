import email
import imp
from re import T
from secrets import choice
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):
          try:
               uid = User.objects.get(email=request.session['email'])
               return render(request,'index.html',{'uid':uid})
          except:
               return render(request,'sign-in.html',{'msg':'Session has Expired.'})

def sign_in(request):
     #return HttpResponse('hello')
     if request.method == 'POST':
          try:
               uid = User.objects.get(email=request.POST['email'])
               if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return redirect('index')
               return render(request,'sign-in.html',{'msg':'Password is Incorrect.'})
          except:
               return render(request,'sign-in.html',{'msg':'Account does not Exists'})
     return render(request,'sign-in.html')

def sign_up(request):
     if request.method == "POST":
          try:
               User.objects.get(email=request.POST['email'])
               msg = "Email Already Exist."
               return render(request,'sign-up.html',{'msg':msg})
          except:
               if request.POST['password'] == request.POST['cpassword']:
                    otp = randrange(1000,9000)
                    subject = 'OTP verification'
                    message = f'Your OTP is {otp}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'], ]
                    send_mail( subject, message, email_from, recipient_list )
                    global temp 
                    temp = {
                         'fname' : request.POST['fname'],
                         'lname' : request.POST['lname'],
                         'email' : request.POST['email'],
                         'mobile' : request.POST['mobile'],
                         'password' : request.POST['password'],
                    }
                    return render(request,'otp.html',{'msg':'OTP sent on your Email !!!.','otp':otp})
               return render(request,'sign-up.html',{'msg':'Both Passwords Are not Same.'})
     return render(request,'sign-up.html')
def otp(request):
     if request.POST['uotp'] == request.POST['otp']:
          global temp
          User.objects.create(
               fname = temp['fname'],
               lname = temp['lname'],
               email = temp['email'],
               mobile = temp['mobile'],
               password = temp['password'],

          )
          del temp
          return render(request,'sign-in.html',{'msg':'Account Created'})
     return render(request,'otp.html',{'msg': 'Invalid OTP','otp':request.POST[otp]})
def profile(request):
     uid = User.objects.get(email=request.session['email'] )
     if request.method ==  'POST':
          uid.fname = request.POST['fname']
          uid.lname = request.POST['lname']
          uid.mobile = request.POST['mobile'][4:]
          uid.save()
          return render(request,'profile.html',{'uid':uid,'msg':'Profile has been Updated'})
     return render(request,'profile.html',{'uid':uid})

def dashboard(request):
     return render(request,'dashboard.html')

def logout(request):
     del request.session['email']
     return render(request,'sign-in.html')

'''def change_password(request):
     if request.method == 'POST':
          try:
               cp= request.POST["cp"]
               np= request.POST["np"]
          
               uid = User.objects.get(email=request.POST['email'])
               check = uid.check_password(np)
               if check == True:
                    pass
                    return render(request,'change-password.html',{'msg':'Password is Correct.'})
               
               else:
                    return render(request,'change-password.html',{'msg':'Password is Incorrect.'})
          except: '''

def forgot_password(request):
     if request.method == 'POST':
          try:
               uid = User.objects.get(email=request.POST['email'])
               s='qwertyiopuasdfghjklzxcvbnm@123456789'
               password = ''.join(choices(s,k=8))
               subject = 'Password Has been Reset.'
               message = f'Your new Password is {password}'
               email_from = settings.EMAIL_HOST_USER
               recipient_list = [request.POST['email'], ]
               send_mail(subject, message, email_from, recipient_list )
               uid.password = password
               uid.save()
               return render(request,'sign-in.html',{'msg':'New password sent on your Email.'})


          except:
               return render(request,'sign-up.html',{'msg':'Account Does not Exists.'})
     return render(request,'forgot-password.html')