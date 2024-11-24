import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.apps import apps



class FeedConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = "feed"

    # connects to socket
    async def connect(self):

        print("WebSocket connection attempt received!")
        try:
            # Add to group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print("(GOOD) WebSocket connection accepted successfully!")

        except Exception as e:
            print(f"Error in connect!!!")
            raise

    # disconnects connection handler
    async def disconnect(self, close_code):
        try:

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(f"(BAD) WebSocket disconnected with code: {close_code}")

        except Exception as e:
            print(f"BAD DISCONNECT")

    # updated to all clients
    async def feed_update(self, event):
        try:
            # sending a lovey message to websocket
            await self.send(text_data=json.dumps(event['data']))
            print("Feed update sent successfully!")

        except Exception as e:
            print(f"BAD feed_update")

    # handle recieving like events!
    async def receive(self, text_data):
            try:
                data = json.loads(text_data)
                if data['type'] == 'like':
                    post_id = data['post_id']
                    user = self.scope["user"]

                    # Update like in database
                    success, likes = await self.update_like(post_id, user)

                    if success:
                        # Broadcast the updated likes to ALL clients
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                "type": "like_update",
                                "post_id": post_id,
                                "likes": likes
                            }
                        )
            except Exception as e:
                print(f"Error in receive: {str(e)}")

    # BROADCASTING like updates!
    async def like_update(self, event):
        try:

            await self.send(text_data=json.dumps({
                "type": "like_update",
                "post_id": event["post_id"],
                "likes": event["likes"]
            }))
        except Exception as e:
            print(f"Error in like_update: {str(e)}")

    @database_sync_to_async
    def update_like(self, post_id, user):

        try:
            Post = apps.get_model('eg_app', 'Post')
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
