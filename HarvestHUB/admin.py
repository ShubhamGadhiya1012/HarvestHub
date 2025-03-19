from django.contrib import admin
from .models import login,admin_login,contact,FarmerDetails,FarmerProduct,AdminPayment,UserPayment

admin.site.register(login)
admin.site.register(admin_login)
admin.site.register(contact)
admin.site.register(FarmerDetails)
admin.site.register(FarmerProduct)  
admin.site.register(AdminPayment) 
admin.site.register(UserPayment) 