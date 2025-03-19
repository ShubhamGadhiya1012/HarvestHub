from django.db import models

class login(models.Model):   
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100,null=False,blank=False)    
    email = models.EmailField(null=False,blank=False)
    password = models.CharField(max_length=100,null=False,blank=False)
    phone_number = models.CharField(max_length=15,null=False,blank=False)
    # profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # terms = models.BooleanField(default=False)
    def __str__(self):        
        return self.name

class admin_login(models.Model):  
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100,null=False,blank=False)    
    email = models.EmailField(null=False,blank=False)
    password = models.CharField(max_length=100,null=False,blank=False)
    phone_number = models.CharField(max_length=15,null=False,blank=False)
    # profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # terms = models.BooleanField(default=False)
    def __str__(self):        
        return self.name


class contact(models.Model):   
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(null=False,blank=False)    
    subject = models.CharField(max_length=100,null=False,blank=False)
    message = models.CharField(max_length=255,null=False,blank=False)
    def __str__(self):        
        return self.name



class FarmerDetails(models.Model):
    id = models.AutoField(primary_key=True) 
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # Consider using Django's built-in auth system instead
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/farmer_personal_photo/')
    land_certificate = models.FileField(upload_to='static/farmer_personal_photo/')
    adhar_card = models.ImageField(upload_to='static/farmer_personal_photo/')
    terms_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class FarmerProduct(models.Model):
    id = models.AutoField(primary_key=True) 
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField()
    quantity = models.IntegerField()
    price = models.CharField(max_length=100)
    # total_amount = models.FloatField(max_length=9999)
    payment = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,default=False,unique=True)
    paymentorder_id = models.CharField(max_length=100,default=False)
    
    order_date = models.CharField(max_length=100,default=False)
    product_image = models.ImageField(upload_to='static/farmer_product/')
    certificate = models.FileField(upload_to='static/farmer_product/')
   

    def __str__(self):
        return f"{self.first_name}"
    

class AdminPayment(models.Model):
    id = models.AutoField(primary_key=True) 
    fname = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=100, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.status}"


class UserPayment(models.Model):
    id = models.AutoField(primary_key=True) 
    uname = models.CharField(max_length=255)
    uemail = models.EmailField()
    phone = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    order_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.status}"
    
    
    

    
    