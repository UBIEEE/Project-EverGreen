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


def index(request):
    if request.user.is_authenticated:
        return render(
            request, "index.html", {"hidden2": "hidden", "email": request.user.email}
        )
    else:
        return render(request, "index.html", {"hidden1": "hidden"})


def get_file_type(file_path: str) -> tuple[str | None, str | None]:
    # returns tuple {type, encoding}
    content_type = mimetypes.guess_type(file_path)
    return content_type


def file_handler(request: HttpRequest, filename: str) -> HttpResponse:
    # can handle img and text

    # get the absolute path
    sanitized_filename = quote(filename)
    path = Path(settings.STATIC_ROOT) / sanitized_filename

    allowed_types: set[str] = {
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

    if not str(path.suffix.lower()) in allowed_types:  # to deal with user uploads
        return HttpResponseNotFound("404 - File type not allowed")

    # deal with /../ attacks
    root_path = Path(settings.STATIC_ROOT).resolve()
    if not path.resolve().is_relative_to(root_path):
        return HttpResponseNotFound("404 Not Found")

    if path.exists() and path.is_file():  # make sure it's not a directory
        content_type, encoding = get_file_type(str(path))

        try:
            with open(path, "rb") as file:
                content = file.read()
        except OSError:  # catch most of them, like FileNotFoundError
            return HttpResponseNotFound("404 Not Found")
            # return render(request, '404.html', status=404) when making 404 pages

        if content_type:
            response = HttpResponse(content, content_type=content_type)
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


def add_cookies(response: HttpResponse, cookies: dict[str, str]) -> HttpResponse:
    """add all cookies from the give dic to the response"""
    for cookie_name, cookie_value in cookies.items():
        response.set_cookie(cookie_name, cookie_value)
    return response


def validate(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseBadRequest()

    password: str = request.POST.get("password", "")
    email: str = request.POST.get("email", "")

    valid_pass = val.validate_password(password)
    valid_email = val.validate_email(email)

    return JsonResponse(
        {"valid_pass": str(valid_pass), "valid_email": str(valid_email)}
    )


def register(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest()

    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    password_confirmation = request.POST.get("confirm_password", "")

    email = html.escape(email)
    password = html.escape(password)
    password_confirmation = html.escape(password_confirmation)

    if val.validate_credentials_on_register(email, password, password_confirmation):
        # Now confirmed valid, create account
        # (Django takes raw password, handles salting/hashing itself before storing)
        new_account = User.objects.create_user(
            username=email, email=email, password=password
        )
        new_account.save()

    # TODO: Should send visible feedback to user

    return HttpResponseRedirect(ROOT_PATH)


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)

    if post.user == request.user:
        post.delete()
    return redirect("/")


def dislike_post(request, pk):
    post = Post.objects.get(pk=pk)

    if post.users_who_liked.contains(request.user):
        post.likes -= 1
        post.users_who_liked.remove(request.user)
        post.save()
    return redirect("/")


def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    # user = request.user.email
    user = "guest@buffalo.edu"
    comment = request.POST["comment"]

    comment = html.escape(comment)

    post_comment = Comments.objects.create(post=post, user=user, comment=comment)
    post_comment.save()
    return redirect("/")


def delete_comment(request, comment_id):
    comment = Comments.objects.get(comment_id)

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

        if str(user) == "hartloff@buffalo.edu":
            target_url = "https://youtube.com/watch?v=JRHARtLZLk8"
            return HttpResponseRedirect(target_url)

        if str(user) == "jesse@buffalo.edu":
            target_url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
            return HttpResponseRedirect(target_url)

        return HttpResponseRedirect(ROOT_PATH)

    return HttpResponseBadRequest()


def update_feed(request) -> JsonResponse:

    posts = Post.objects.all().order_by("-timestamp")
    posts_data = []
    current_user = request.user
    for post in posts:
        post_dict = {
            "id": post.id,
            "user": post.user,
            "image": {"url": post.image.url if post.image else ""},
            "caption": post.caption + "\n",
            "likes": post.likes,
            "likers_display": post.get_likers_display(),
            "has_liked": current_user.is_authenticated
            and post.users_who_liked.filter(id=current_user.id).exists(),
            "comments": [],
        }
        posts_data.append(post_dict)

    return JsonResponse({"posts": posts_data})


def like_post(request, pk) -> JsonResponse:
    user_who_is_liking = request.user

    if request.method == "POST":
        try:
            post = Post.objects.get(pk=pk)

            if str(
                user_who_is_liking.username
            ) != "AnonymousUser" and not post.users_who_liked.contains(
                user_who_is_liking
            ):
                post.likes += 1
                post.users_who_liked.add(user_who_is_liking)
            elif str(user_who_is_liking.username) != "AnonymousUser":
                post.likes -= 1
                post.users_who_liked.remove(user_who_is_liking)
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
