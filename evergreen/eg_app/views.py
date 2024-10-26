from django.shortcuts import render

import eg_app.util.validators as val

from django.http import JsonResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

ROOT_PATH = "/"

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
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        passwordConf = request.POST.get("confirm_password", "")

        # Make sure passwords match
        if password != passwordConf:
            return HttpResponseRedirect(ROOT_PATH)
        
        # Make sure email & pwd are valid
        if not (val.validate_email(email, True) and val.validate_password(password)):
            return HttpResponseRedirect(ROOT_PATH)

        # Make sure email doesn't already exist
        if len(User.objects.filter(email=email)) != 0:
            return HttpResponseRedirect(ROOT_PATH)
        
        # Now confirmed valid, create account
        newAcct = User.objects.create_user(username=email, email=email, password=password)
        newAcct.save()

        # TODO: Should send visible feedback to user

        return HttpResponseRedirect(ROOT_PATH)
    
    return HttpResponseBadRequest()

def login_view(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
        else:
            # TODO: Should send visible feedback to user
            pass

        return HttpResponseRedirect(ROOT_PATH)
    
    return HttpResponseBadRequest()

def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(ROOT_PATH)
