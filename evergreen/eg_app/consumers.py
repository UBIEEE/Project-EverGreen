import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class FeedConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = "feed"  # Define the group name as a class attribute

    async def connect(self):
        print("WebSocket connection attempt received!") # Debug print
        try:
            # Add to group
            await self.channel_layer.group_add(
                self.room_group_name,  # Use the defined group name
                self.channel_name
            )
            await self.accept()
            print("WebSocket connection accepted successfully!")
        except Exception as e:
            print(f"Error in connect: {str(e)}")
            raise

    async def disconnect(self, close_code):
        try:
            # Remove from group
            await self.channel_layer.group_discard(
                self.room_group_name,  # Use the defined group name
                self.channel_name
            )
            print(f"WebSocket disconnected with code: {close_code}")
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    async def feed_update(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps(event['data']))
            print("Feed update sent successfully!")
        except Exception as e:
            print(f"Error in feed_update: {str(e)}")