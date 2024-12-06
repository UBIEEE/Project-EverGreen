import base64
import html
import json
import uuid
from imghdr import what

# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# from channels.layers import get_channel_layer
from django.apps import apps
from django.core.files.base import ContentFile


class FeedConsumer(AsyncWebsocketConsumer):
    MAX_FRAME_SIZE = 8000000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = "feed"
        self.buffer = b""
        self.upload_size = 0

    # connects to socket
    async def connect(self):

        print("WebSocket connection attempt received!")

        # Add to group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("(GOOD) WebSocket connection accepted successfully!")

    # disconnects connection handler
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"(BAD) WebSocket disconnected with code: {close_code}")

    # updated to all clients
    async def feed_update(self, event):

        # sending a lovey message to websocket
        await self.send(
            text_data=json.dumps(
                {"type": "feed_update", "posts": event["data"]["posts"]}
            )
        )
        print("Feed update sent successfully!")

    # handle receiving like events!
    async def receive(self, text_data=None, bytes_data=None):

        # check to see if FRAME is greater than 8MB
        if text_data and len(text_data.encode()) > self.MAX_FRAME_SIZE:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": f"(txt)Too high. Limit: {self.MAX_FRAME_SIZE}MB",
                    }
                )
            )
            return
        # same here, but with text content. It should stop premature, so no upload.
        if bytes_data and len(bytes_data) > self.MAX_FRAME_SIZE:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": f"(bytes)To high. Limit: {self.MAX_FRAME_SIZE}MB",
                    }
                )
            )
            return

        try:
            data = json.loads(text_data)
            if data["type"] == "like":
                post_id = data["post_id"]
                user = self.scope["user"]

                # Update like in database
                success, likes = await self.update_like(post_id, user)

                if success:
                    post_data = await self.get_post_data(post_id)

                    # Broadcast the updated likes to ALL clients
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "like_update",
                            "post_id": post_id,
                            "likes": post_data["likes"],
                            "likers_display": post_data["likers_display"],
                            "has_liked": post_data["has_liked"],
                        },
                    )
            elif data["type"] == "upload_post":

                post = await self.handle_post_upload(data)

                if post:
                    # BROADCAST TO ALL CLIENTS
                    posts_data = await self.get_all_posts()

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "feed_update",
                            "data": {"posts": posts_data},
                        },
                    )

                    # send upload
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "upload_response",
                                "status": "success",
                                "post_id": str(post.id),
                            }
                        )
                    )
        except Exception as e:
            print(f"Error in receive: {str(e)}")

    @database_sync_to_async
    def get_all_posts(self):

        Post = apps.get_model("eg_app", "Post")

        posts = Post.objects.all().order_by("-timestamp")

        all_posts_data = []

        for post in posts:
            current_user = self.scope["user"]

            post_image_url = ""

            if post.image and hasattr(post.image, "url"):
                post_image_url = post.image.url

            user_has_liked = False

            if current_user.is_authenticated:
                user_has_liked = post.userLikes.filter(id=current_user.id).exists()

            post_data = {
                "id": str(post.id),
                "user": post.user,
                "image": {"url": post_image_url},
                "caption": post.caption + "\n",  # Add newline after caption
                "likes": post.likes,
                "likers_display": post.get_likers_display(),
                "has_liked": user_has_liked,
                "comments": [],  # start w/ empty!
            }

            all_posts_data.append(post_data)

        # Return the complete list of post data
        return all_posts_data

    @database_sync_to_async
    def handle_post_upload(self, data):
        Post = apps.get_model("eg_app", "Post")

        try:
            user = self.scope["user"]
            if str(user.username) == "AnonymousUser":
                print("MUST BE LOGGED IN")
                return None

            caption = data.get("caption", "")
            MAX_CHAR_LENGTH = 280

            if len(caption) > MAX_CHAR_LENGTH:
                return None

            post_data = {
                "user": html.escape(user.email),
                "caption": html.escape(data.get("caption", "")),
            }

            # Handle image if it is present *no tautology*
            if (
                data.get("image")
                and data.get("image") != "data:application/octet-stream;base64,"
            ):

                # Remove the data URL prefix
                format, imgstr = data["image"].split(";base64,")
                image_bytes = base64.b64decode(imgstr)

                MAX_IMAGE_SIZE = 8000000

                if len(image_bytes) > MAX_IMAGE_SIZE:
                    return None

                # check the magic bytes!
                image_type = what(None, h=image_bytes)

                if image_type not in ["jpeg", "jpg", "png", "gif"]:
                    return None

                # Generate unique filename
                filename = f"{uuid.uuid4()}.{image_type}"

                # Convert base64 to file
                image_data = ContentFile(image_bytes, name=filename)
                post_data["image"] = image_data

            post = Post.objects.create(**post_data)
            return post

        except Exception as e:
            print(f"Error creating post: {str(e)}")
            return None

    @database_sync_to_async
    def get_post_data(self, post_id):
        Post = apps.get_model("eg_app", "Post")
        try:
            post = Post.objects.get(pk=post_id)
            user = self.scope["user"]
            has_liked = (
                str(user.username) != "AnonymousUser"
                and post.userLikes.filter(id=user.id).exists()
            )

            return {
                "likes": post.likes,
                "likers_display": post.get_likers_display(),
                "has_liked": has_liked,
            }
        except Post.DoesNotExist:
            return None

    # BROADCASTING like updates!

    async def like_update(self, event):
        try:
            post_data = await self.get_post_data(event["post_id"])

            if post_data:
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "like_update",
                            "post_id": event["post_id"],
                            "likes": post_data["likes"],
                            "likers_display": post_data["likers_display"],
                            "has_liked": post_data["has_liked"],
                        }
                    )
                )
        except Exception as e:
            print(f"Error in like_update: {str(e)}")

    @database_sync_to_async
    def get_post(self, post_id):
        Post = apps.get_model("eg_app", "Post")
        return Post.objects.get(pk=post_id)

    @database_sync_to_async
    def update_like(self, post_id, user):
        Post = apps.get_model("eg_app", "Post")
        try:

            post = Post.objects.get(pk=post_id)

            if str(user.username) != "AnonymousUser":

                if not post.userLikes.contains(user):
                    post.likes += 1
                    post.userLikes.add(user)

                else:
                    post.likes -= 1
                    post.userLikes.remove(user)

                post.save()

                return True, post.likes
            return False, post.likes

        except Post.DoesNotExist:
            return False, 0
