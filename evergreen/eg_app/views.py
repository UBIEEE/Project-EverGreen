from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.conf import settings
import mimetypes
from pathlib import Path
from urllib.parse import quote


import eg_app.util.validators as val

from django.http import JsonResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
# from eg_app.models import Email
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

ROOT_PATH = "/"

# Create your views here.

# handles request 
def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html',{'hidden2': 'hidden', 'email': request.user.email})
    else:
        return render(request,'index.html',{'hidden1': 'hidden'})

def getFileType(filePath: str) -> tuple[str|None, str|None]:
    contentType = mimetypes.guess_type(filePath) #returns tuple {type, encoding}
    return contentType

def fileHandler(request: HttpRequest, fileName: str) -> HttpResponse:  # can handle img and text
    # get the absolute path
    sanitizedFileName = quote(fileName)
    path = Path(settings.STATIC_ROOT) / sanitizedFileName

    allowedType: set[str] = {'.css', '.html', '.js', '.png', '.jpg', '.jpeg', '.gif', '.mp3', '.mp4', '.xml', '.json', '.pdf', '.ico'}  # can add more

    if not str(path.suffix.lower()) in allowedType:  # to deal with user uploads
        return HttpResponseNotFound("404 - File type not allowed")

    # deal with /../ attacks
    rootPath = Path(settings.STATIC_ROOT).resolve()
    if not path.resolve().is_relative_to(rootPath):
        return HttpResponseNotFound("404 Not Found")

    if path.exists() and path.is_file(): # make sure it's not a directory
        contentType, encoding = getFileType(str(path))

        try:
            with open(path, 'rb') as file:
                content = file.read()
        except OSError:  # catch most of them, like FileNotFoundError
            return HttpResponseNotFound("404 Not Found")
            # return render(request, '404.html', status=404) when making 404 pages

        if contentType:
            response = HttpResponse(content, content_type=contentType)
        else:
            response = HttpResponse(content)

        if encoding:
            response['Content-Encoding'] = encoding
        else:
            response['Content-Encoding'] = ""

        response['X-Content-Type-Options'] = "nosniff"
        # response['Content-Length'] = str(len(content))  # needed for very large files, Django handles it

        return response
    else:
        return HttpResponseNotFound("404 Not Found")

def addCookies(response: HttpResponse, cookies: dict[str, str]):
    """add all cookies from the give dic to the response"""
    for cookieName, cookieValue in cookies.items():
        response.set_cookie(cookieName, cookieValue)
    return response

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
        if user:
            login(request, user)
        else:
            # TODO: Should send visible feedback to user
            pass

        return HttpResponseRedirect(ROOT_PATH)
    
    return HttpResponseBadRequest()

@csrf_exempt
def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(ROOT_PATH)
