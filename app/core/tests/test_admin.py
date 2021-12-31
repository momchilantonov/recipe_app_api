from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):

    def setUp(self):
        admin_email = 'admin@admin.com'
        admin_password = 'adminPass'
        user_email = 'user@user.com'
        user_password = 'userPass'
        user_name = 'User'

        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email=admin_email,
            password=admin_password,
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email=user_email,
            password=user_password,
            name=user_name,
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
