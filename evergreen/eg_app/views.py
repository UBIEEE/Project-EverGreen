from django.shortcuts import render

import eg_app.util.validators as val

from django.http import JsonResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# handles request 
def index(request):
    return render(request,'index.html')

@csrf_exempt
def validate(request):
    if request.method == "POST":


        password = request.POST.get("password")
        email = request.POST.get("email")



        valid_pass = True
        valid_email = True

        if not val.validate_password(password):
            valid_pass = False

        if not val.validate_email(email):
            valid_email = False


        return JsonResponse({"valid_pass":str(valid_pass),"valid_email":str(valid_email)})
    
    return HttpResponseBadRequest()

def register(request: HttpRequest):
    root = '/'

    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        passwordConf = request.POST.get("confirm_password", "")

        if password != passwordConf:
            # Make sure passwords match
            return HttpResponseRedirect(root)
        
        if not (val.validate_email(email, True) and val.validate_password(password)):
            # Make sure email & pwd are valid
            return HttpResponseRedirect(root)

        # Now confirmed valid, create account
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            newAcct = User.objects.create_user(email, email, password)
            newAcct.save()

        # TODO: Should send visible feedback to user

        return HttpResponseRedirect(root)
    
    return HttpResponseBadRequest()

def login_view(request: HttpRequest):
    root = '/'

    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
        else:
            # TODO: Should send visible feedback to user
            pass

        return HttpResponseRedirect(root)
    
    return HttpResponseBadRequest()

def logout_view(request: HttpRequest):
    logout(request)
    root = "/"
    return HttpResponseRedirect(root)
