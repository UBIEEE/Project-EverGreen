from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.conf import settings
import mimetypes
from pathlib import Path
from urllib.parse import quote


import eg_app.util.validators as val

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# handles request 
def index(request):
    return render(request,'index.html')

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



