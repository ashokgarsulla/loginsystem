from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from loginsystem import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .token import generate_token
from django.contrib.auth import views 
# Create your views here.


def home(request):
    return render(request, "auth/Index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "username already Exists")
            return redirect('home')
       # if User.objects.filter(email = email):
        #    messages.error(request,"Email Aready exists")
        #    return redirect('home')
        if len(username) > 10:
            messages.error(request, "username must be under 10 characters")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Password didn't match!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        print('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
        print(myuser)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(
            request, 'your account has been succesfully created! and We have sent you a confirmation email, please confirm your account in order to activate your account')

        # Welcome email code

        subject = "Welcome to Ashok garsulla -  Login System!"
        message = "Hello " + myuser.first_name + "!!\n" + "Welcome to Our Login System \n" + "Thank you for Visiting our Website\n" + \
            "We have also  sent a confirmation email, Please confirm your email address in order to activate your account.\n\n Thanking You\n\nAshok Garsulla"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email Code
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        print(myuser.pk)
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ AG-logoinSystem"
        conf_message = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            conf_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silenty = True
        email.send()
        return redirect("signin")
    return render(request, "auth/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        print("singnin----------------------------------------------")
        print(user)
        print(type(user))

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'auth/Index.html', {'fname': fname})
        else:
            messages.error(request, 'Bad Credential Please try again!')
            return redirect('signin')
    return render(request, "auth/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "loged out successfully.....")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return render(request, 'email_acctivated.html')
    else:
        return render(request, 'activation_failed.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        myuser = User.objects.filter(email=email).values().get()
        myuser = myuser['username']
        print(myuser)
        if User.objects.filter(email=email):
            messages.success(request, "Link has been sent " + email+ ".")
            print("________+____________")
            print(myuser)
            print(myuser.first_name)
            current_site = get_current_site(request)
            print(current_site)
            email_subject = "password reset @ AG-logoinSystem"
            reset_message = render_to_string('password_reset_email.html', {
                'name': myuser['first_name'],
                'email': myuser['email'],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                reset_message,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.fail_silenty = True
            email.send()
            return redirect('forgot')
        else:
            messages.error(request, "Account doen't exist in " + email + ", Please enter correct email id  ")
            current_site = get_current_site(request)
            email_subject = "password reset @ AG-logoinSystem"
            reset_message = render_to_string('password_reset_email.html', {
                'name': myuser.first_name,
                'email': myuser.email,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                reset_message,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silenty = True
            email.send()
            return redirect('forgot')
    return render(request,'forgot_password.html')


def password_reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return render(request, 'email_acctivated.html')
    else:
        return render(request, 'activation_failed.html')
