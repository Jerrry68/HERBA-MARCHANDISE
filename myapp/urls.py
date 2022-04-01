from . import views 
from django.urls import path

urlpatterns = [

   
    path('',views.sign_in, name='sign-in'),
    path('index/',views.index, name='index'),
    path('sign_up/',views.sign_up, name='sign-up'),
    path('otp/',views.otp, name='otp'),
    path('logout/',views.logout, name='logout'),
    path('profile/',views.profile,name='profile'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('forgot_password/',views.forgot_password,name='forgot-password'),
    #path('change_password/',views.change_password,name='change-password'),
    
]