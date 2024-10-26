from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
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

def getFileType(filePath):
    contentType = mimetypes.guess_type(filePath)[0] #first idx == the type
    return contentType

def fileHandler(request, fileName): # can handle img and text
    # get the absolute path
    sanitizedFileName = quote(fileName)
    path = Path(settings.STATIC_ROOT) / sanitizedFileName

    allowedType = {'.css', '.html', '.js', '.png', '.jpg', '.jpeg', '.gif', '.mp3', '.mp4', '.xml', '.json', '.pdf','.ico'} # can add more, 

    if not str(path.suffix.lower()) in allowedType: # to deal with user uploads
        return HttpResponseNotFound("404 - File type not allowed")

    #deal with /../ attacks
    rootPath = Path(settings.STATIC_ROOT).resolve() #
    if not path.resolve().is_relative_to(rootPath):
        return HttpResponseNotFound(f"404 Not Found")

    if path.exists() and path.is_file(): # make sure its not a directory
        contentType = getFileType(path)
        
        try:
            with open(path, 'rb') as file:
                content = file.read()

            response = HttpResponse(content, content_type=contentType)
            response['X-Content-Type-Options'] = "nosniff"
            #response['Content-Length'] = str(len(content)) is need for very large file, django handles is not

            #print(response)
        
            return response
        
        except OSError as e: # catch most of em, like FileNotFoundError  
            return HttpResponseNotFound(f"404 Not Found")
            #return render(request, '404.html', status=404) when make 404 pages 

    else:
        return HttpResponseNotFound("404 Not Found")
    
def addCookies(response, cookies): # add all cookies from the give dic to the response
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



