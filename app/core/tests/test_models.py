from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def setUp(self):
        self.email = "test@test.com"
        self.password = "testpass123"

    def test_create_user_with_emai_succesful(self):
        """Test creating user with email is succseful"""
        test_email = "test@test.com"
        test_password = "testpass123"
        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
        )

        self.assertEqual(user.email, test_email)
        self.assertTrue(user.check_password(test_password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        test_email = "test@TEST.com"
        user = get_user_model().objects.create_user(
            email=test_email,
            password=self.password,
        )

        self.assertEqual(user.email, test_email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise an error"""
        test_email = None

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=test_email,
                password=self.password,
            )

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            email=self.email,
            password=self.password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
