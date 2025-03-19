"""
URL configuration for HarvestHUB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.MainPage),
     
    path('registration/', view.Registration,name='registration'),
    path('login/', view.Login,name='login'),
    path('home/',view.HomePage,name='home'),
    path('about/',view.about,name='about'),
    path('contact/',view.contactus,name='contact'),
    path('services/',view.service,name='services'),
    path('emailverify/',view.emailverify,name='emailverify'),
    path('otpverify/',view.otpverify,name="otpverify"),


    path('harvestcart/', view.HarvestCart,name='harvestcart'),
    path('harvestkirana/', view.HarvestKirana,name='harvestkirana'),
    path('harvestmandi/', view.HarvestMandi,name='harvestmandi'),
    path('harvestglobal/', view.HarvestGlobal,name='harvestglobal'),

    path('orderbooking/<int:id>/', view.OrderBooking,name='orderbooking'),
    path('usercreate_order/<int:id>/', view.User_createorder, name='usercreate_order'),
    path('userpayment_success/', view.Userpayment_success, name='userpayment_success'),
    path('userprofile/', view.Userprofile,name='userprofile'),\
    path('download-invoice/<int:user_id>/', view.download_invoice, name='download_invoice'),

#--------------------- farmer -------------------------------------
    path('farmerlogin/', view.farmerlogin,name='farmerlogin'),
    path('farmeremailverify/',view.farmeremailverify,name='farmeremailverify'),
    path('farmerotpverify/',view.farmerotpverify,name="farmerotpverify"),
    path('farmerregistration/',view.farmerregistration,name="farmerregistration"),
    path('farmerdashboard', view.farmerdashboard, name='farmerdashboard'),
    path('farmersellproduct/', view.farmer_sellproduct,name='farmersellproduct'),
    path('farmerviewproduct/', view.farmer_viewproduct,name='farmerviewproduct'),
    path('farmercontact/', view.farmer_contact,name='farmercontact'),
    path('farmerprofile/', view.farmer_profile,name='farmerprofile'),
    path('deletefarmerproduct/<int:id>/', view.farmerproduct_delete, name='deletefarmerproduct'),
    path('updatefarmerproduct/', view.update_farmer_product, name='updatefarmerproduct'),


    

#------------------ admin -------------------------------------------

    path('admin_login/',view.admin_Login,name="admin_login"),
    path('admin_registration/',view.admin_Registration,name="admin_registration"),

    path('admin_dashboard/',view.admin_dashboard,name="admin_dashboard"),
    path('admin_farmer/',view.admin_farmer,name="admin_farmer"),
    path('admin_products/',view.admin_products,name="admin_products"),
    path('admin_user/',view.admin_user,name="admin_user"),
    path('admin_feedback/',view.admin_feedback,name="admin_feedback"),
    path('deletefeedback/<int:id>/', view.feedback_delete, name='feedback_delete'),
    path('deleteuser/<int:id>/', view.user_delete, name='user_delete'),
    path('deletefarmer/<int:id>/', view.farmer_delete, name='farmer_delete'),
    path('adminprofileview/<int:id>/',view.admin_profileview,name='adminprofileview'),
    path('adminviewproductdetails/<int:id>/',view.admin_viewproductdetails,name='adminviewproductdetails'),

    path('admincreate_order/<int:id>/', view.Admin_createorder, name='admincreate_order'),
    path('payment_success/', view.payment_success, name='payment_success'),
   
    
    
]


