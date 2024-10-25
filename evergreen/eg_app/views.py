from django.shortcuts import render

import eg_app.util.validators as val

from django.http import JsonResponse, HttpRequest, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from eg_app.util import authenticate as auth

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
        result, reason = auth.register(email, password)

        # TODO: Should send visible feedback to user

        return HttpResponseRedirect(root)

def login(request: HttpRequest):
    root = '/'

    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        
        # Try to log in
        token = auth.login(email, password)

        if token == "":
            return HttpResponseRedirect(root)
        else:
            response = HttpResponseRedirect(root)
            response["Auth-Token"] = token
            return response
