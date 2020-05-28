from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from main.tests.functions import sample_user, get_user_detail_url


TOKEN_URL = reverse("user:token")


USER_URL = reverse("user:users-list")


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            "username": "name",
            "password": "testpass",
            "email": "test@mail.com",
        }
        response = self.client.post(USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)

        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_exists(self):
        payload = {
            "username": "Test username",
            "password": "testpass123",
            "email": "test@test.com",
        }

        sample_user(**payload)
        response = self.client.post(USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.get(username=payload["username"])

        self.assertTrue(user)

    def test_password_too_short(self):
        payload = {
            "username": "Test username",
            "email": "test@test.com",
            "password": "pass",
        }
        response = self.client.post(USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(len(payload["password"]) < 8)

        exists = get_user_model().objects.filter(username=payload["username"]).exists()

        self.assertFalse(exists)

    def test_create_token_success(self):
        payload = {
            "username": "Test username",
            "email": "test@test.com",
            "password": "password123",
        }
        sample_user(**payload)

        response = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        payload = {
            "username": "Test username",
            "email": "test@test.com",
            "password": "password123",
        }

        sample_user("Test username", "test@test.com", "incorrectpass")

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {"username": "Test username", "password": "password123"}

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        payload = {"username": "Test username", "password": ""}

        sample_user("Test username", "test@test.com", "testpass123")

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthorizedUserApiTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        response = self.client.get(get_user_detail_url(self.user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "username": self.user.username,
                "email": self.user.email,
                "id": self.user.id,
            },
        )

    def test_update_other_user_not_allowed(self):

        user2 = sample_user("user2", "pass123")

        response = self.client.patch(
            get_user_detail_url(user2.id), {"username": "edited"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_profile_success(self):
        payload = {
            "username": "newtestusername",
            "email": "newtest@test.com",
            "password": "newpassword123",
        }

        response = self.client.put(get_user_detail_url(self.user.id), payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, payload["username"])
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
