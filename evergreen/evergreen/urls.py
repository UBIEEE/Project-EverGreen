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

from django.contrib import admin
from django.urls import path
from eg_app import views
from django.conf.urls.static import static
from django.conf import settings


#from evergreen import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index,name='index'),
    path('validate',views.validate,name='validate'), # type: ignore
    path('updateFeed',views.updateFeed,name="updateFeed"),
    path('uploadPost',views.uploadPost,name="uploadPost"),
    path('deletePost',views.deletePost,name="deletePost"),
    path('likePost',views.likePost,name="likePost"),
    path('dislikePost',views.dislikePost,name="dislikePost"),
    path('addComment',views.addComment,name="addComment"),
    path('deleteComment',views.deleteComment,name="deleteComment"),
]
