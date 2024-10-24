from django.shortcuts import render

import eg_app.util.validators as val

from django.http import JsonResponse

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



