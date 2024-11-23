import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Post
from django.core import serializers

# this handles the websockets channels

class FeedConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.channel_layer.group_add("feed", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("feed", self.channel_name)

    
    # this method will allow to do anything we want on data we get
    # nothing need for now
    async def receive(self, text_data):
       
        pass
    
    # updates feed for the web sockets
    async def feed_update(self, event):
        
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_feed_data(self):
        posts = Post.objects.all().order_by("-timestamp")
        posts_data = []
        
        
        for post in posts:
            
            if post.image:
                image_dict = {"url": post.image.url}
            else:
                image_dict = {"url": ""}
            
            post_dict = {
                "id": str(post.id),
                "user": post.user,
                "image": image_dict,
                "caption": post.caption + "\n",
                "likes": post.likes,
                "comments": [],
            }
            
            posts_data.append(post_dict)
            
        return {"posts": posts_data}