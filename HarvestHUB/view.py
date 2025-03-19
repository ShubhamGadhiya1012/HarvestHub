from django.http import HttpResponse
from django.shortcuts import render ,get_object_or_404, redirect
from django.core.mail import send_mail 
from django.conf import settings 
from .forms import EmailForm
import random 
from django.db.models import Sum
import razorpay
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import login,admin_login,contact,FarmerDetails,FarmerProduct,AdminPayment,UserPayment
from django.core.exceptions import MultipleObjectsReturned
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime


from django.contrib import messages


def MainPage(request):
    return render(request,"Mainpage.html")

def Registration(request):
    if request.method == 'POST':
        Email = request.POST.get('Email')
        Name = request.POST.get('Name')
        PhoneNumber = request.POST.get('PhoneNumber')
        Password = request.POST.get('Password')
        print(Email, Name, PhoneNumber, Password)
        user = login(name=Name, email=Email, password=Password, phone_number=PhoneNumber)
        user.save()
        return redirect('home')  # Replace 'home' with the actual name of your home URL
    else:
        return render(request, 'user_registration.html')

        # if request.method == 'POST':
        #     form = UserForm(request.POST, request.FILES)
        #     if form.is_valid():
        #       form.save()
        #       return redirect('home') 
        #  # Redirect to the same URL to avoid form resubmission
        # else:
        #     form = UserForm()
        
        # Retrieve all user records

        # users = login.objects.all()  
        # return render(request, 'register.html')

       




  



def Login(request):
      
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        try:
            user = login.objects.get(email=email)
            if user.password == password:
                # Login successful
                request.session['email'] = email
                return redirect('home')  # Replace 'dashboard' with the actual dashboard URL
            else:
                # Incorrect password
                return render(request, 'user_login.html', {'error': 'Invalid Password'})
        except login.DoesNotExist:
            # User not found
            return render(request, 'user_login.html', {'error': 'User does not exist'})
        
        except MultipleObjectsReturned:
            # Handle multiple users with the same email
            return render(request, 'user_login.html', {'error': 'Multiple accounts with this email. Please contact support.'})
    else:
            return render(request,"user_login.html")



def HomePage(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(email, name, subject, message)
        user = contact(name=name,email=email, subject=subject, message=message)
        user.save()
        return redirect('contact')  
    else:
        return render(request, 'contact.html')

def service(request):
    return render(request,"services.html")


def send_otp(email):
    otp = random.randint(100000, 999999) 
   
    subject = 'Your OTP Code' 
    message = f'Your OTP code is {otp}.' 
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [email] 
    send_mail(subject, message, email_from, recipient_list) 
    return otp 
    

def emailverify(request):
    if request.method == 'POST': 
        form = EmailForm(request.POST) 
        if form.is_valid(): 
            email = form.cleaned_data['email'] 

            if login.objects.filter(email=email).exists():
                return render(request, 'FarmerEmailverify.html', {'error': 'Email already registered.'})

            request.session['email'] = email
            otp = send_otp(email) 
            request.session['otp'] = otp 
            return redirect('otpverify') 
    else: 
        form = EmailForm() 
    return render(request, 'Emailverify.html', {'form': form}) 
   
    



def otpverify(request):
    if request.method == 'POST':
        otp = ''.join(request.POST.getlist('otp[]'))
        if otp == str(request.session.get('otp')): 
            return redirect('registration')
        else:
            return render(request, 'Otpverify.html', {'error': 'Invalid OTP'})
    return render(request, 'Otpverify.html')



def admin_Registration(request):
    if request.method == 'POST':
        Email = request.POST.get('Email')
        Name = request.POST.get('Name')
        PhoneNumber = request.POST.get('PhoneNumber')
        Password = request.POST.get('Password')
        print(Email, Name, PhoneNumber, Password)

        try:
               
            if admin_login.objects.filter(email=Email).exists():
                return render(request, 'admin_registration.html', { 'error': 'Email already registered'})
                
            user = admin_login(name=Name, email=Email, password=Password, phone_number=PhoneNumber)
            user.save()
            return redirect('admin_dashboard')  
        
        except MultipleObjectsReturned:
               
                return render(request, 'admin_registration.html', {'error': 'Multiple accounts with this email. Please contact support.'})
    else:
        return render(request, 'admin_registration.html')

       
def admin_Login(request):
      
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        try:
            user = admin_login.objects.get(email=email)
            if user.password == password:
               
                return redirect('admin_dashboard') 
            else:
               
                return render(request, 'admin_login.html', {'error': 'Invalid Password'})
        except admin_login.DoesNotExist:
           
            return render(request, 'admin_login.html', {'error': 'User does not exist'})
        except MultipleObjectsReturned:
           
            return render(request, 'admin_login.html', {'error': 'Multiple accounts with this email. Please contact support.'})
    else:
            return render(request,"admin_login.html")
    

def HarvestCart(request):
    farmer_products = FarmerProduct.objects.all() 
    return render(request, 'HarvestCart.html', {'farmer_products': farmer_products})
   

def HarvestMandi(request):
    farmer_products = FarmerProduct.objects.all() 
    return render(request, 'HarvestMandi.html', {'farmer_products': farmer_products})

def HarvestKirana(request):
    farmer_products = FarmerProduct.objects.all() 
    return render(request, 'HarvestKirana.html', {'farmer_products': farmer_products})
  

def HarvestGlobal(request):
    farmer_products = FarmerProduct.objects.all() 
    return render(request, 'HarvestGlobal.html', {'farmer_products': farmer_products})
   

def OrderBooking(request,id):
    uemail =  request.session['email']
    user = login.objects.get(email=uemail)
    fp = FarmerProduct.objects.get(id=id)

    return render(request,"OrderBooking.html",{'user' :user,'fp': fp})


def User_createorder(request, id):
    if request.method == "POST":
       
        cname = request.POST.get('cname')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        pname = request.POST.get('pname')
        price = float(request.POST.get('price'))
        quantity = int(request.POST.get('quantity'))
        total_amount = float(request.POST.get('total_amount')) * 100 
        request.session['orderemail'] = cemail
        request.session['ordername'] = cname
        request.session['orderpname'] = pname
        request.session['orderprice'] = price
        request.session['orderquantity'] = quantity
        request.session['orderamount'] = total_amount/100
        
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        razorpay_order = client.order.create({
            "amount": total_amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        
        payment = UserPayment(
            uname=cname,
            uemail = cemail,
            phone = cphone,
            product_name = pname,
            price = price,
            quantity = quantity,
            order_id=razorpay_order['id'],
            amount=total_amount / 100, 
            status="Pending"
        )
        payment.save()
        

        

        callback_url = reverse('userpayment_success')
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_API_KEY,
            'amount': total_amount,
            'currency': 'INR',
            'callback_url': callback_url,
        }

        return render(request, 'Userpayment.html', context)

    return redirect('home') 


@csrf_exempt
def Userpayment_success(request):

    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')

        try:
            payment = UserPayment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = payment_id
            payment.status = 'Success'
            payment.save()

            oemail = request.session['orderemail']
            oname = request.session['ordername']
            opname = request.session['orderpname']
            oprice =  request.session['orderprice'] 
            oqun = request.session['orderquantity'] 
            orderamount = request.session['orderamount'] 

            
            subject = 'Order Confirmation - Your HarvestHUB Order Has Been Placed!' 

            message = f"""
            Dear {oname},
            Thank you for shopping with HarvestHUB! Your order has been successfully placed,
            and we’re excited to deliver fresh organic products directly to your doorstep.

            Here are the details of your order:

            - Product Name: {opname}
            - Quantity: {oqun}KG
            - Price per Unit: ₹{oprice}
            - Total Amount Paid: ₹{orderamount}
            - Payment Status: Paid

            We’re committed to ensuring that you receive the highest quality products, straight from trusted farmers.
            If you have any questions or need assistance, please feel free to contact us at support@harvesthub.com or call us at +91-9898457047.

            Thank you for choosing HarvestHUB to support organic farming and sustainable living!

            Best Regards,  
            The HarvestHUB Team
            """

            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [oemail] 

            send_mail(subject, message, email_from, recipient_list) 

        except UserPayment.DoesNotExist :
            pass
        return redirect('userprofile') 
    return redirect('userprofile')


def Userprofile(request):
    email =  request.session.get('email')
    datas = UserPayment.objects.filter(uemail=email)  
    total_orders = datas.count()
    total_amount = datas.aggregate(Sum('amount'))['amount__sum']
    datas2 = login.objects.filter(email=email) 
    user = datas2.first()    
    return render(request, 'User_profile.html', {'datas': datas ,'total_orders': total_orders,
        'total_amount': total_amount,'user' :user})
  
  
def download_invoice(request, user_id):
    try:
        user = UserPayment.objects.get(id=user_id)
        template = get_template('invoice_template.html')
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d') 
        current_time = current_datetime.strftime('%H:%M:%S') 
        context = {'user': user,
                    'current_date': current_date,  
            'current_time': current_time,  
            }
        html = template.render(context)
        print(html)  # Debug: Print HTML to inspect
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{user_id}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    except UserPayment.DoesNotExist:
        return HttpResponse('User payment not found.')


#--------------------- admin panel--------------------------------------------------


def admin_dashboard(request):

    datas = contact.objects.all()  
    no_feedback = datas.count() 
    datas2 = login.objects.all()  
    no_users = datas2.count()  
    datas3 = FarmerDetails.objects.all()  
    no_farmer = datas3.count()  
    order = UserPayment.objects.all()  
    total_amount = order.aggregate(Sum('amount'))['amount__sum']
     
    return render(request, 'Admin_dashboard.html', {'no_feedback': no_feedback,'no_users': no_users,'no_farmer': no_farmer,'order':order,'total_amount':total_amount})
  

def admin_farmer(request):
    datas = FarmerDetails.objects.all() 
    return render(request,"Admin_farmer.html", {'datas': datas})

def admin_feedback(request):
    datas = contact.objects.all()  
    return render(request, 'Admin_feedback.html', {'datas': datas})


def admin_products(request):
    datas = FarmerProduct.objects.all() 
    
    for data in datas:
        try:
            price = float(data.price)
            quantity = float(data.quantity)
            data.total_amount = price * quantity
        except ValueError:
            data.total_amount = 0.00
    return render(request,"Admin_products.html", {'datas': datas})
    


def admin_profileview(request,id):
    farmerdetails = get_object_or_404(FarmerDetails, pk=id)  
    return render(request, 'AdminProfileview.html', {'fd': farmerdetails})

def admin_viewproductdetails(request,id):
    farmerdetails = get_object_or_404(FarmerProduct, pk=id)
    total_amount = 0.00
    
    try:
        price = float(farmerdetails.price)
        quantity = float(farmerdetails.quantity)
        total_amount = price * quantity
    except ValueError:
        total_amount = 0.000

    return render(request, 'Admin_Viewproductdetails.html', {'fd': farmerdetails, 'tm': total_amount})


def admin_user(request):
    datas = login.objects.all()  
    return render(request, 'Admin_user.html', {'datas': datas})

def feedback_delete(request, id):
    record = get_object_or_404(contact, id=id)
    record.delete()
    return redirect('admin_feedback')

def user_delete(request, id):
    record = get_object_or_404(login, id=id)
    record.delete()
    return redirect('admin_user')

def farmer_delete(request, id):
    record = get_object_or_404(FarmerDetails, id=id)
    record.delete()
    return redirect('admin_farmer')


def Admin_createorder(request,id):
    
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    pdetails = get_object_or_404(FarmerProduct, pk=id)
    total_amount = 0.00
    try:
        price = float(pdetails.price)
        quantity = float(pdetails.quantity)
        total_amount = price * quantity*100
    except ValueError:
        total_amount = 0.000
    
   
    razorpay_order = client.order.create({
        "amount": total_amount,
        "currency": "INR",
        "payment_capture": "1"
    })

   
    payment = AdminPayment(
        fname = pdetails.first_name,
        order_id=razorpay_order['id'],
        amount=total_amount /100
    )
    payment.save()

   

    pdetails = get_object_or_404(FarmerProduct, pk=id)
    pdetails.paymentorder_id = razorpay_order['id']

    pdetails.save()
    callback_url = reverse('payment_success')
    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_API_KEY,
        'amount': total_amount,
        'currency': 'INR',
        'callback_url': callback_url,
        
    }
    return render(request, 'Admin_payment.html',context )


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')

        try:
            payment = AdminPayment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = payment_id
            payment.status = 'Success'
            payment.save()

            payment_status = FarmerProduct.objects.get(paymentorder_id=razorpay_order_id)
            payment_status.payment = 'Success'
            payment_status.save()
        except AdminPayment.DoesNotExist or FarmerProduct.DoesNotExist:
            # Handle the case where the payment or product is not found
            pass

        return redirect('admin_products')
    return redirect('admin_products')








# ----------------------------- farmer---------------------------------

def farmerlogin(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        try:
            user = FarmerDetails.objects.get(email=email)
            if user.password == password:
                # Login successful
                request.session['femail'] = email
                return redirect('farmerdashboard')  # Replace 'farmerdashboard' with the actual dashboard URL
            else:
                # Incorrect password
                return render(request, 'FarmerLogin.html', {'error': 'Invalid Password'})
        
        except FarmerDetails.DoesNotExist:
            # User not found
            return render(request, 'FarmerLogin.html', {'error': 'User does not exist'})
        
        except MultipleObjectsReturned:
            # Handle multiple users with the same email
            return render(request, 'FarmerLogin.html', {'error': 'Multiple accounts with this email. Please contact support.'})
    
    else:
        return render(request, "FarmerLogin.html")





def farmeremailverify(request):
    if request.method == 'POST': 
        form = EmailForm(request.POST) 
        if form.is_valid(): 
            email = form.cleaned_data['email'] 

            if FarmerDetails.objects.filter(email=email).exists():
                return render(request, 'FarmerEmailverify.html', {'error': 'Email already registered.'})

            request.session['femail'] = email
            otp = send_otp(email) 
            request.session['otp'] = otp 
            return redirect('farmerotpverify') 
    else: 
        form = EmailForm() 
    return render(request, 'FarmerEmailverify.html', {'form': form}) 


def farmerotpverify(request):
    if request.method == 'POST':
        otp = ''.join(request.POST.getlist('otp[]'))  # Combine the OTP inputs
        if otp == str(request.session.get('otp')):  # Compare with the OTP stored in session
            return redirect('farmerregistration')
        else:
            return render(request, 'Otpverify.html', {'error': 'Invalid OTP'})
    return render(request, 'FarmerOtpverify.html')

def farmerregistration(request):

    if request.method == 'POST':
        # Extract data from the form
        email = request.POST.get('personal-email')
        phone = request.POST.get('personal-phone')
        password = request.POST.get('personal-password')
        first_name = request.POST.get('contact-first_name')
        last_name = request.POST.get('contact-last_name')
        age = request.POST.get('contact-age')
        gender = request.POST.get('contact-gender')
        address = request.POST.get('contact-address')
        city = request.POST.get('contact-city')
        state = request.POST.get('contact-state')
        zipcode = request.POST.get('contact-zipcode')
        country = request.POST.get('contact-country')
        terms_accepted = request.POST.get('security-terms_accepted') == 'on'

        # Handle file uploads
        image = request.FILES.get('contact-image')
        land_certificate = request.FILES.get('contact-land_certificate')
        adhar_card = request.FILES.get('contact-adhar_card')

        # Create and save the FarmerDetails instance
        farmer = FarmerDetails(
            email=email,
            phone=phone,
            password=password,  # Remember to hash the password in a real-world scenario
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            country=country,
            image=image,
            land_certificate=land_certificate,
            adhar_card=adhar_card,
            terms_accepted=terms_accepted
        )
        farmer.save()
        return redirect('farmerdashboard')  # Create a success page and add its URL to urls.py
    email = request.session['femail']
    return render(request, 'Farmer_registration.html', {'femail': email})


def farmerdashboard(request):
    
    return render(request, 'FarmerDashboard.html')




def farmer_sellproduct(request):
    email =  request.session.get('femail')
    fdata = FarmerDetails.objects.get(email=email)
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('fname')
        email = request.POST.get('fmail')
        phone = request.POST.get('phn')
        product_name = request.POST.get('proname')
        product_desc = request.POST.get('prodesc')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        payment = request.POST.get('payment')
        order_id = request.POST.get('order_id')
        order_date = request.POST.get('order_date')
        

        # Handle file uploads
        product_image = request.FILES.get('pimage')
        certificate = request.FILES.get('poimage')

        # Create and save the FarmerDetails instance
        farmerproduct = FarmerProduct(
            first_name=first_name,
            email=email,
            phone=phone,
            product_name=product_name,
            product_desc=product_desc,
            quantity=quantity,
            price=price,
            payment=payment,
            order_id = order_id,
            order_date = order_date,
            product_image=product_image,
            certificate=certificate
        )
        farmerproduct.save()
        return redirect('farmersellproduct')  
    return render(request, 'FarmerSellproduct.html',{'fdata': fdata})

def farmer_viewproduct(request):
    email = request.session.get('femail')
    datas = FarmerProduct.objects.filter(email=email)  # Returns a queryset (iterable)
      
    for data in datas:
        try:
            price = float(data.price)
            quantity = float(data.quantity)
            data.total_amount = price * quantity
        except ValueError:
            data.total_amount = 0.00

    return render(request, 'FarmerViewproduct.html', {'datas': datas})

def update_farmer_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        farmer_product = FarmerProduct.objects.get(id=product_id)
        
        farmer_product.first_name = request.POST.get('first_name')
        farmer_product.product_name = request.POST.get('product_name')
        farmer_product.quantity = request.POST.get('quantity')
        farmer_product.price = request.POST.get('price')

        # Save the updated product
        farmer_product.save()

        return redirect('farmerviewproduct')

def farmer_contact(request):
    return render(request, 'FarmerContact.html')
    
def farmer_profile(request):
    email =  request.session.get('femail')
    farmerdetails = get_object_or_404(FarmerDetails, email=email)  
    return render(request, 'FarmerProfile.html', {'fd': farmerdetails})

def farmerproduct_delete(request, id):
    record = get_object_or_404(FarmerProduct, id=id)
    record.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('farmerviewproduct')
    


