from django.shortcuts import render, redirect
import eg_app.util.validators as val
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from eg_app.models import Post, Comments

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

def updateFeed(request):

    posts = Post.objects.all().order_by('-timestamp')
    posts_data = []
    for post in posts:
        post_dict = {
            'id': post.id,
            'user': post.user,
            'image': {'url': post.image.url if post.image else ''},
            'caption': post.caption,
            'likes': post.likes,
            'comments': []
        }
        posts_data.append(post_dict)

    return JsonResponse({'posts': posts_data})

def uploadPost(request):
    # user = request.user.email
    user = 'guest@buffalo.edu'
    image = request.FILES.get("image upload")
    caption = request.POST["caption"]

    post = Post.objects.create(user=user, image=image, caption=caption)
    post.save()
    return redirect("/")

def deletePost(request, pk):
    post = Post.objects.get(pk=pk)

    if post.user == request.user:
        post.delete()
    return redirect("/")

def likePost(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.userLikes.contains(request.user):
        post.likes += 1
        post.userLikes.add(request.user)
        post.save()
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
    user = 'guest@buffalo.edu'
    comment = request.POST["comment"]

    postComment = Comments.objects.create(post=post, user=user, comment=comment)
    postComment.save()
    return redirect("/")

def deleteComment(request, commentId):
    comment = Comments.objects.get(commentId)

    if comment.user == request.user:
        comment.delete()
    return redirect("/")
