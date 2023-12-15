from django.shortcuts import render ,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# 
from django.core.mail import send_mail,EmailMultiAlternatives,BadHeaderError
from django.core import mail
from django.core.mail.message import EmailMessage
from django.conf import settings

# user activate
from django.views.generic import View
from account.utils import generate_token   #create util file,
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
# thread
import threading

class EmailThread(threading.Thread):
    def __init__(self,email_msg):
        self.email_msg=email_msg
        threading.Thread.__init__(self)
    def run(self):
        self.email_msg.send()

    
# Create your views here.
def signup(request):
    if request.method=="POST":
        username=request.POST['email']
        name=request.POST['name']
        password=request.POST['pass']
        confirm_password=request.POST['pass1']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'account/signup.html')
        try:
            if User.objects.get(username=username):
                messages.warning(request,"UserName is Taken")
                return render(request,'account/signup.html')

        except Exception as e:
            messages.warning(request,e)
        try:
            user = User.objects.create_user(username,name,password)
            user.is_active=False
            user.save()
            # activate user

            current_site=get_current_site(request)
            email_subject="Activate your Account"
            message=render_to_string('account/activate.html',{
                'user':user,
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })
            email_msg=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[username],)
            EmailThread(email_msg).start()
            messages.info(request,"Please Verify Your Email,Check Your Inbox")
            return render(request,"account/login.html")
        except Exception as e:
            pass
    return render(request,"account/signup.html")    
    

def handle_login(request):
    if request.method=="POST":
        username=request.POST['username']
        userpassword=request.POST['pass1']
        user=authenticate(username=username,password=userpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Login Success")
            return render(request,'index.html')

        else:
            messages.error(request,"invalid Credentials ")
            return redirect("/account/login/")

    return render(request,"account/login.html")


        
class Activate(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as e:
            pass
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated ")
            return redirect("/account/login/")
        return render(request,"account/activate_fail.html")


@login_required(redirect_field_name="/account/login/")
def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect("/account/login/")


from django.contrib.auth.tokens import PasswordResetTokenGenerator

class resetPassword(View):
    def get(self,request):
        return render(request,'account/reset-password.html')
    def post(self,request):
        if request.method=="POST":
            email=request.POST['email']
            user=User.objects.filter(username=email)
            try:
                if user.exists:
                    current_site=get_current_site(request)
                    email_subject="Reset Your Password"
                    message=render_to_string('account/reset-password-mail.html',{
                        'user':user,
                        'domain':'127.0.0.1:8000',
                        'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                        'token':PasswordResetTokenGenerator().make_token(user[0])
                    })
                    email_msg=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
                    EmailThread(email_msg).start()
                    messages.info(request," Reset Email Sent Successful")
                    return render(request,'account/reset-password.html')
            except Exception as e:
                messages.info(request,e)
            return render(request,'account/reset-password.html')

class setNewPassword(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link IS Invalid | Please Retry |")
                return render(request,'account/reset-password.html')
        except DjangoUnicodeDecodeError as e:
            messages.warning(request,e)
        return render(request,'account/reset-password-page.html',context)
    
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass']
        confirm_password=request.POST['pass1']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'reset-password-page.html')
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success | Please Login With New Password")
            return redirect('/account/login/')
        except DjangoUnicodeDecodeError as e:
            messages.warning(request,e) 
            return render(request,'reset-password-page.html',context)
        
