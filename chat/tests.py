from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Conversation


User = get_user_model()


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")
        self.user = User.objects.create_user(username="testuser",
                                             password="strongpassword123")
        self.client.force_login(self.user)

    def test_home_view_get(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_view_context(self):
        response = self.client.get(self.home_url)
        self.assertIn("users", response.context)
        self.assertEqual(list(response.context["users"]),
                         list(User.objects.all()))


class CreateConversationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1",
                                              password="password123")
        self.user2 = User.objects.create_user(username="user2",
                                              password="password123")
        self.create_conversation_url = reverse("create-conversation", args=[self.user2.id])

    def test_create_conversation_authenticated(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.create_conversation_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         reverse("chat-room", kwargs={"conversation_id": Conversation.objects.first().id}))


class ChatRoomViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
        self.chat_room_url = reverse("chat-room", args=[self.conversation.id])

    def test_chat_room_authenticated(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.chat_room_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "room.html")
