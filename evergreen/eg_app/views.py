import html
import mimetypes
import traceback
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

import eg_app.util.validators as val
from eg_app.models import Comments, Post

ROOT_PATH = "/"

# Create your views here.

# handles request


@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        return render(
            request, "index.html", {"hidden2": "hidden", "email": request.user.email}
        )
    else:
        return render(request, "index.html", {"hidden1": "hidden"})


def getFileType(filePath: str) -> tuple[str | None, str | None]:
    # returns tuple {type, encoding}
    contentType = mimetypes.guess_type(filePath)
    return contentType


def fileHandler(request: HttpRequest, fileName: str) -> HttpResponse:
    # can handle img and text

    # get the absolute path
    sanitizedFileName = quote(fileName)
    path = Path(settings.STATIC_ROOT) / sanitizedFileName

    allowedType: set[str] = {
        ".css",
        ".html",
        ".js",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".mp3",
        ".mp4",
        ".xml",
        ".json",
        ".pdf",
        ".ico",
    }  # can add more

    if not str(path.suffix.lower()) in allowedType:  # to deal with user uploads
        return HttpResponseNotFound("404 - File type not allowed")

    # deal with /../ attacks
    rootPath = Path(settings.STATIC_ROOT).resolve()
    if not path.resolve().is_relative_to(rootPath):
        return HttpResponseNotFound("404 Not Found")

    if path.exists() and path.is_file():  # make sure it's not a directory
        contentType, encoding = getFileType(str(path))

        try:
            with open(path, "rb") as file:
                content = file.read()
        except OSError:  # catch most of them, like FileNotFoundError
            return HttpResponseNotFound("404 Not Found")
            # return render(request, '404.html', status=404) when making 404 pages

        if contentType:
            response = HttpResponse(content, content_type=contentType)
        else:
            response = HttpResponse(content)

        if encoding:
            response["Content-Encoding"] = encoding

        response["X-Content-Type-Options"] = "nosniff"
        # response['Content-Length'] = str(len(content))  # needed for very large
        # files, Django handles it

        return response
    else:
        return HttpResponseNotFound("404 Not Found")


def addCookies(response: HttpResponse, cookies: dict[str, str]) -> HttpResponse:
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

        return JsonResponse(
            {"valid_pass": str(valid_pass), "valid_email": str(valid_email)}
        )

    return HttpResponseBadRequest()


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        passwordConf = request.POST.get("confirm_password", "")

        email = html.escape(email)
        password = html.escape(password)
        passwordConf = html.escape(passwordConf)

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
        # (Django takes raw password, handles salting/hashing itself before storing)
        newAcct = User.objects.create_user(
            username=email, email=email, password=password
        )
        newAcct.save()

        # TODO: Should send visible feedback to user

        return HttpResponseRedirect(ROOT_PATH)

    return HttpResponseBadRequest()


def deletePost(request, pk):
    post = Post.objects.get(pk=pk)

    if post.user == request.user:
        post.delete()
    return redirect("/")


def dislikePost(request, pk):
    post = Post.objects.get(pk=pk)

    if post.userLikes.contains(request.user):
        post.likes -= 1
        post.userLikes.remove(request.user)
        post.save()
    return redirect("/")


def addComment(request, postId):
    post = Post.objects.get(id=postId)
    # user = request.user.email
    user = "guest@buffalo.edu"
    comment = request.POST["comment"]

    comment = html.escape(comment)

    postComment = Comments.objects.create(post=post, user=user, comment=comment)
    postComment.save()
    return redirect("/")


def deleteComment(request, commentId):
    comment = Comments.objects.get(commentId)

    if comment.user == request.user:
        comment.delete()
    return redirect("/")


def login_view(request: HttpRequest):
    if request.method == "POST":

        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        email = html.escape(email)

        password = html.escape(password)

        user = authenticate(request, username=email, password=password)
        if user:
            # Django handles all the storing and sending of auth tokens itself
            login(request, user)
        else:
            # TODO: Should send visible feedback to user
            pass

        return HttpResponseRedirect(ROOT_PATH)

    return HttpResponseBadRequest()


@csrf_exempt
def updateFeed(request) -> JsonResponse:

    posts = Post.objects.all().order_by("-timestamp")
    posts_data = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "user": post.user,
            "image": {"url": post.image.url if post.image else ""},
            "caption": post.caption + "\n",
            "likes": post.likes,
            "comments": [],
        }
        posts_data.append(post_dict)

    return JsonResponse({"posts": posts_data})


@csrf_exempt
def uploadPost(request) -> JsonResponse:
    if request.method == "POST":

        user = request.user.email

        # Match THE NAME IN THE UPLOAD
        image = request.FILES.get("image_upload")
        caption = request.POST.get("caption")

        caption = html.escape(caption)

        if image and caption:
            post = Post.objects.create(user=user, image=image, caption=caption)
            post.save()

            return JsonResponse(
                {"status": "success", "image_url": post.image.url, "post_id": post.id}
            )
        elif caption:
            post = Post.objects.create(user=user, caption=caption)
            post.save()
            return JsonResponse({"status": "success", "post_id": post.id})
        else:
            return JsonResponse(
                {"status": "error", "message": "Missing image or caption"}, status=400
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@csrf_exempt
def likePost(request, pk) -> JsonResponse:
    user_who_is_liking = request.user

    if request.method == "POST":
        try:
            post = Post.objects.get(pk=pk)

            if str(
                user_who_is_liking.username
            ) != "AnonymousUser" and not post.userLikes.contains(user_who_is_liking):
                post.likes += 1
                post.userLikes.add(user_who_is_liking)
            elif str(user_who_is_liking.username) != "AnonymousUser":
                post.likes -= 1
                post.userLikes.remove(user_who_is_liking)
            post.save()
            return JsonResponse({"status": "success", "likes": post.likes})

        except Post.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Post not found"}, status=404
            )

        except Exception:
            print(traceback.format_exc())
            return JsonResponse(
                {"status": "error", "message": "An internal error occurred"}, status=500
            )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@csrf_exempt
def logout_view(request: HttpRequest):
    # Django handles the invalidating and client-side removal of auth tokens itself
    logout(request)
    return HttpResponseRedirect(ROOT_PATH)
