"""
URL configuration for evergreen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from eg_app import views
from eg_app.consumers import FeedConsumer




from eg_app import views

# from evergreen import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("validate", views.validate, name="validate"),
    path("updateFeed", views.updateFeed, name="updateFeed"),
    path("uploadPost", views.uploadPost, name="uploadPost"),
    path("deletePost", views.deletePost, name="deletePost"),
    #path("likePost/<uuid:pk>", views.likePost, name="likePost"),
    # path('dislikePost',views.dislikePost,name="dislikePost"),
    path("addComment", views.addComment, name="addComment"),
    path("deleteComment", views.deleteComment, name="deleteComment"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    #path("ws/", include("eg_app.routing")),
    #re_path(r'^ws/feed/$', FeedConsumer.as_asgi()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # FOR PROD, or DEBUG=FALSE
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
