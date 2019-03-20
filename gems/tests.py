from django.test import TestCase
from gems.models import Category, User, UserProfile
from gems.forms import UserForm, UserProfileForm
import gems.test_utils as test_utils

# Create your tests here.

class CategoryMethodTests(TestCase):
    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add
        a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
    
class Chapter9ModelTests(TestCase):
    def test_user_profile_model(self):
        # Create a user
        user, user_profile = test_utils.create_user()

        # Check there is only the saved user and its profile in the database
        all_users = User.objects.all()
        self.assertEquals(len(all_users), 1)

        all_profiles = UserProfile.objects.all()
        self.assertEquals(len(all_profiles), 1)

        # Check profile fields were saved correctly
        all_profiles[0].user = user
        all_profiles[0].website = user_profile.website