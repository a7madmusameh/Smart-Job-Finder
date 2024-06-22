from django.urls import path
from . import views

urlpatterns = [
    path('',views.Homepage,name='Homepage'),
    path('HomeCom',views.HomeCom,name='HomeCom'),
    path('HomeUser',views.HomeUser,name='HomeUser'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('SignupUser',views.SignupUser,name='SignupUser'),
    path('SignupCompany',views.SignupCompany,name='SignupCompany'),
    path('contactus',views.contactus,name='contactus'),
    path('contactusCom',views.contactusCom,name='contactusCom'),
    path('contactusUser',views.contactusUser,name='contactusUser'),
    path('employeer',views.employeer,name='employeer'),
    path('ProfileUser',views.ProfileUser,name='ProfileUser'),
    path('ProfileCompany',views.ProfileCompany,name='ProfileCompany'),
    path('resultsearchemployee',views.resultsearchemployee,name='resultsearchemployee'),
    path('EditeDataUser',views.EditeDataUser,name='EditeDataUser'),
    path('EditeDataCompany',views.EditeDataCom,name='EditeDataCom'),
]
