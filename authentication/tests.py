from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123"
        }

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_signup_view_post_success(self):
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_signup_view_post_invalid(self):
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "differentpassword"
        response = self.client.post(self.signup_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser").exists())


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.login_data = {
            "username": "testuser",
            "password": "strongpassword123",
        }
        self.user = User.objects.create_user(
            username=self.login_data["username"],
            password=self.login_data["password"],
            first_name="Test",
            last_name="User",
            email="testuser@example.com"
        )
        self.err_msg = "Please enter a correct username and password."

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(reverse("home")))

    def test_login_view_post_invalid_password(self):
        invalid_data = self.login_data.copy()
        invalid_data["password"] = "wrongpassword"
        response = self.client.post(self.login_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.err_msg)

    def test_login_view_post_nonexistent_user(self):
        invalid_data = self.login_data.copy()
        invalid_data["username"] = "nonexistentuser"
        response = self.client.post(self.login_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.err_msg)
