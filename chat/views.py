import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Conversation

logger = logging.getLogger("chat")
api_logger = logging.getLogger("api")


@login_required
def home_view(request):
    context = User.objects.all()
    context = {
        "users": User.objects.all(),
    }
    return render(request, "home.html", context)


@login_required
def create_conversation(request, other_user_id):
    api_logger.info(f"HTTP {request.method} {request.path}")
    try:
        other_user = User.objects.get(id=other_user_id)
        logger.info(f'User {request.user.username} creating conversation with {other_user.username}')
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).distinct().first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, other_user)

        return redirect("chat-room", conversation_id=conversation.id)
    except Exception as e:
        logger.error(f'Error creating conversation between {request.user.username} and user ID {other_user_id}: {e}')
        return render(request, 'error.html', {'error': 'Could not create conversation'})


@login_required
def chat_room(request, conversation_id):
    api_logger.info(f"HTTP {request.method} {request.path}")
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        logger.info(f'User {request.user.username} accessing chat room {conversation_id}')
        return render(request, "room.html", {"conversation": conversation, "user": request.user})
    except Exception as e:
        logger.error(f'Error accessing chat room {conversation_id} for user {request.user.username}: {e}')
        return render(request, 'chat/error.html', {'error': 'Could not access chat room'})
