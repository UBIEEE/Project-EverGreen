import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

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
            # sending message to websocket
            await self.send(text_data=json.dumps(event['data']))
            print("Feed update sent successfully!")
            
        except Exception as e:
            print(f"BAD feed_update")