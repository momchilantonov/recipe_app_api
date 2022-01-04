from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='user@user.com', password='userPass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag as string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.0
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Tet that the image is saved in correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
