from django.urls import path
from .views import home_view, create_conversation, chat_room


urlpatterns = [
    path("", home_view, name="home"),
    path("create/<int:other_user_id>/", create_conversation, name="create-conversation"),
    path("<int:conversation_id>/", chat_room, name="chat-room"),
]
