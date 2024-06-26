import json
import logging
import redis
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache

from channels.generic.websocket import AsyncWebsocketConsumer


logger = logging.getLogger("chat")
redis_instance = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_name = f"chat_{self.conversation_id}"
        logger.info(f"User {self.user.username} connecting to room {self.room_name}")

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        messages = self.get_message_history()
        await self.send(text_data=json.dumps({
            "messages": messages
        }))
        logger.info(f"Sent message history for room {self.room_name}")

    async def disconnect(self, close_code):
        logger.info(f"User {self.user.username} disconnecting from room {self.room_name}")
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        user_cache_key = f"user_{self.user.id}_chat_throttle"
        current_time = datetime.now()
        last_access_time = cache.get(user_cache_key)
        message_count = cache.get(f"{user_cache_key}_count", 0)

        if last_access_time and current_time - last_access_time < timedelta(minutes=1):
            if message_count >= 10:
                cache.set(f"{user_cache_key}_count", 0, timeout=60)
                cache.set(user_cache_key, current_time, timeout=60)
                await self.send(text_data=json.dumps({
                    "message": "Messsage limit reached. Retry after 10 seconds.",
                    "username": "Connection closed"
                }))
                await self.close(code=4001)
                return

        cache.set(user_cache_key, current_time, timeout=60)
        cache.set(f"{user_cache_key}_count", message_count + 1, timeout=60)

        data = json.loads(text_data)
        message = data["message"]
        username = self.user.username

        self.save_message(username, message)
        logger.info(f"Saved message from user {username} in room {self.room_name}")

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat.message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))
        logger.info(f"Sent message to WebSocket for user {username} in room {self.room_name}")

    def save_message(self, username, message):
        try:
            redis_instance.rpush(self.room_name, json.dumps({
                "username": username,
                "message": message
            }))
            logger.info(f"Message saved in Redis for room {self.room_name}")
        except Exception as e:
            logger.error(f"Error saving message in Redis for room {self.room_name}: {e}")

    def get_message_history(self):
        try:
            messages = redis_instance.lrange(self.room_name, 0, -1)
            logger.info(f"Retrieved message history for room {self.room_name}")
            return [json.loads(msg) for msg in messages]
        except Exception as e:
            logger.error(f"Error retrieving message history for room {self.room_name}: {e}")
            return []
