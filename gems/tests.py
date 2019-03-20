from django.test import TestCase
from gems.models import Category, Gem, User, UserProfile
from gems.forms import UserForm, UserProfileForm, GemForm
from django.core.urlresolvers import reverse
import gems.test_utils as test_utils
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings

# 
class CategoryMethodTests(TestCase):
    def test_category_slug_creation(self):
        """
        slug_line_creation check to make sure that when an admin
        adds a new category, an appropriate slug line is created,
        i.e. "Test Category String" -> "test-category-string"
        """
        cat = Category(name='Test Category String')
        cat.save()
        self.assertEqual(cat.slug, 'test-category-string')
        
# 
class GemMethodTests(TestCase):
    def test_gem_slug_creation(self):
         # Create a test category
        category = Category(name="Category 1")
        category.save()
        
         # Create a test gem
        gem = Gem(category=category, name='Test Gem Name With Many Words')
        gem.save()
        
        # Test gem slug
        self.assertEqual(gem.slug, 'test-gem-name-with-many-words')

# 
class UserModelTests(TestCase):
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
        all_profiles[0].profile_image = user_profile.profile_image

# 
class CategoryModelTests(TestCase):
    def test_adding_category_works(self):
        # Create a test category
        category = Category(name="Category 1", description="Description 1")
        category.save()
        
        #Check slug was generated
        self.assertEquals(category.slug, "category-1")

        #Check there is only one category
        categories = Category.objects.all()
        self.assertEquals(len(categories), 1)

        #Check attributes were saved correctly
        categories[0].name = "Category 1"
        categories[0].description = "Description 1"
        categories[0].slug = category.slug

# 
class GemModelTests(TestCase):
    def test_adding_gem_works(self):
        # CONTINUE HERE
        pass

# 
class IndexViewTests(TestCase):
    def test_index_contains_most_liked_gems(self):
        response = self.client.get(reverse('index'))
        self.assertIn('Most Liked Gems'.lower(), response.content.decode('ascii').lower())

    def test_index_contains_most_recent_gems(self):
        response = self.client.get(reverse('index'))
        self.assertIn('Most Liked Gems'.lower(), response.content.decode('ascii').lower())
        
    def test_contactus_contains_our_email(self):
        # Check if the given message is in Contact us
        self.client.get(reverse('index'))
        response = self.client.get(reverse('contact_us'))
        info = "Please send us an email to adminteam@glasgowgems.com " \
               "and we will be back in touch as soon as possible."
        self.assertIn(info.lower(), response.content.decode('ascii').lower())

# 
class GemViewTests(TestCase):
    def test_add_gem_form_is_displayed_correctly(self):
        # Create user and log in - only logged in user can add a gem (different test)
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')
        
        # Access add category page
        response = self.client.get(reverse('add_gem'))

        # Check form in response context is instance of GemForm
        self.assertTrue(isinstance(response.context['form'], GemForm))

        # Check form is displayed correctly
        # Header
        self.assertIn('Add a new Gem!'.lower(), response.content.decode('ascii').lower())

        # Input
        self.assertIn('Name:', response.content.decode('ascii'))
        self.assertIn('Address:', response.content.decode('ascii'))
        self.assertIn('Category:', response.content.decode('ascii'))
        self.assertIn('Upload image:', response.content.decode('ascii'))
        self.assertIn('Image source:', response.content.decode('ascii'))
        self.assertIn('Description:', response.content.decode('ascii'))

        # Check Add Gem button
        self.assertIn('type="submit"', response.content.decode('ascii'))
        self.assertIn('name="submit"', response.content.decode('ascii'))
        self.assertIn('value="Add Gem"', response.content.decode('ascii'))
        
    def test_access_gem_that_does_not_exist(self):
        # Create a test category
        category = Category(name="Category 1")
        category.save()
        
        # Access a gem that does not exist in the created category
        response = self.client.get(reverse('show_gem', args=[category.slug, 'DNE']))

        # Check if there is a response (status code OK is 200)
        self.assertEquals(response.status_code, 200)

        # Check the rendered page informs about non-existent gems
        self.assertIn('The specified gem does not exist!', response.content.decode('ascii'))

# 
class CategoryViewTests(TestCase):
    def test_access_category_that_does_not_exist(self):
        # Access a category that does not exist
        response = self.client.get(reverse('show_category', args=['DNE']))

        # Check if there is a response (status code OK is 200)
        self.assertEquals(response.status_code, 200)

        # Check the rendered page informs about non-existent category
        self.assertIn('The specified category does not exist!', response.content.decode('ascii'))

#
class UserAuthViewTests(TestCase):
    def test_registration_form_is_displayed_correctly(self):
        #Access registration page
        try:
            response = self.client.get(reverse('sign_up'))
        except:
            try:
                response = self.client.get(reverse('gems:sign_up'))
            except:
                return False

        # Check if form is rendered correctly
        self.assertIn('Register for Glasgow Gems'.lower(),
                      response.content.decode('ascii').lower())
        self.assertIn('Username'.lower(),
                      response.content.decode('ascii').lower())
        self.assertIn('Email Address'.lower(),
                      response.content.decode('ascii').lower())
        self.assertIn('Password'.lower(),
                      response.content.decode('ascii').lower())
        self.assertIn('Profile image'.lower(),
                      response.content.decode('ascii').lower())

        # Check form in response context is instance of UserForm
        self.assertTrue(isinstance(response.context['user_form'], UserForm))

        # Check form in response context is instance of UserProfileForm
        self.assertTrue(isinstance(response.context['profile_form'], UserProfileForm))

        user_form = UserForm()
        profile_form = UserProfileForm()

        # Check form is displayed correctly
        self.assertEquals(response.context['user_form'].as_p(), user_form.as_p())
        self.assertEquals(response.context['profile_form'].as_p(), profile_form.as_p())

        # Check submit button
        self.assertIn('type="submit"', response.content.decode('ascii'))
        self.assertIn('name="submit"', response.content.decode('ascii'))
        self.assertIn('value="Register"', response.content.decode('ascii'))
        
    def test_login_form_is_displayed_correctly(self):
        #Access login page
        try:
            response = self.client.get(reverse('login'))
        except:
            try:
                response = self.client.get(reverse('gems:login'))
            except:
                return False

        #Check form display

        #Username label and input text
        self.assertIn('Username:', response.content.decode('ascii'))
        self.assertIn('input type="text"', response.content.decode('ascii'))
        self.assertIn('name="username"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="25"', response.content.decode('ascii'))

        #Password label and input text
        self.assertIn('Password:', response.content.decode('ascii'))
        self.assertIn('input type="password"', response.content.decode('ascii'))
        self.assertIn('name="password"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="25"', response.content.decode('ascii'))

        #Enter button
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="Enter"', response.content.decode('ascii'))
        
        #Sign Up button
        self.assertIn("Don't have an account?", response.content.decode('ascii'))
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="Sign Up"', response.content.decode('ascii'))
    
    def test_login_provides_error_message(self):
        # Access login page
        try:
            response = self.client.post(reverse('login'), {'username': 'wronguser',
                                                           'password': 'wrongpass'})
        except:
            try:
                response = self.client.post(reverse('gems:login'), {'username': 'wronguser',
                                                                    'password': 'wrongpass'})
            except:
                return False
        # get error message from redirect
        error_message = (list(response.wsgi_request._messages))[0]
        # check if it's equal to the required error message
        self.assertEqual(str(error_message), 'Username or password incorrect. Try again.')
    
    def test_login_redirects_to_index(self):
        # Create a user
        test_utils.create_user()

        # Access login page via POST with user data
        try:
            response = self.client.post(reverse('login'), {'username': 'testuser',
                                                           'password': 'test1234'})
        except:
            try:
                response = self.client.post(reverse('gems:login'), {'username': 'testuser',
                                                                    'password': 'test1234'})
            except:
                return False

        # Check if redirected to index after login
        self.assertRedirects(response, reverse('index'))
        
    def test_upload_image(self):
        # Create a user and image to upload to register user
        image = SimpleUploadedFile("testuser.jpg", b"file_content", content_type="image/jpeg")
        try:
            response = self.client.post(reverse('sign_up'),
                             {'username': 'testuser', 'password':'test1234',
                              'email': 'testuser@testuser.com',
                              'profile_image': image})
        except:
            try:
                response = self.client.post(reverse('gems:sign_up'),
                                 {'username': 'testuser', 'password':'test1234',
                                  'email': 'testuser@testuser.com',
                                  'profile_image': image})
            except:
                return False

        # Check user was successfully registered
        # CHANGE MESSAGES TO SOMETHING MORE SENSIBLE
        self.assertIn('Thanks for registering!'.lower(),
                      response.content.decode('ascii').lower())
        user = User.objects.get(username='testuser')
        user_profile = UserProfile.objects.get(user=user)
        path_to_image = './media/profile_images/testuser.jpg'
        
        # Check image was saved properly
        self.assertTrue(os.path.isfile(path_to_image))

        # Delete image created
        default_storage.delete('./media/profile_images/testuser.jpg')

# 
class TemplateTests(TestCase):
    def test_base_template_exists(self):
        # Check base.html exists inside template folder
        path_to_base = settings.TEMPLATE_DIR + '/gems/base.html'
        self.assertTrue(os.path.isfile(path_to_base))
        
    def test_titles_displayed(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Create a test category
        category = Category(name="Category 1")
        category.save()
        
        # Create a test gem
        gem = Gem(category=category, name="Gem 1")
        gem.save()

        # Access index and check the title displayed
        response = self.client.get(reverse('index'))
        self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        self.assertIn('Home'.lower(), response.content.decode('ascii').lower())

        # Access category page and check the title displayed
        response = self.client.get(reverse('show_category', args=[category.slug]))
        self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        self.assertIn(category.name.lower(), response.content.decode('ascii').lower())
        
        # Access gem page and check the title displayed
        response = self.client.get(reverse('show_gem', args=[category.slug, gem.slug]))
        self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        self.assertIn(gem.name.lower(), response.content.decode('ascii').lower())
 
        # Access add a gem page and check the title displayed
        response = self.client.get(reverse('add_gem'))
        self.assertIn(('Glasgow Gems - ').lower(), response.content.decode('ascii').lower())
        self.assertIn('Add a Gem'.lower(), response.content.decode('ascii').lower())
        
        # Access search results page and check the title displayed
        response = self.client.get(reverse('search_results'))
        self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        self.assertIn('Search results'.lower(), response.content.decode('ascii').lower())
        
        # Access log in page and check the title displayed
        response = self.client.get(reverse('login'))
        self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        self.assertIn('Log In'.lower(), response.content.decode('ascii').lower())
 
        # Access sign up page and check the title displayed
        response = self.client.get(reverse('sign_up'))
        self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        self.assertIn('Sign Up'.lower(), response.content.decode('ascii').lower())
        
        #=======================================================================
        # ONCE PROFILE IS IN
        # # Access profile page and check the title displayed
        # response = self.client.get(reverse('profile'))
        # self.assertIn('Glasgow Gems - '.lower(), response.content.decode('ascii').lower())
        # self.assertIn('Profile'.lower(), response.content.decode('ascii').lower())
        #=======================================================================
        
    def test_pages_using_templates(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Create a test category
        category = Category(name="Category 1")
        category.save()
        
        # Create a test gem
        gem = Gem(category=category, name="Gem 1")
        gem.save()
        
        # Create a list of pages to access
        pages = [reverse('index'), reverse('show_category', args=[category.slug]),
                 reverse('show_gem', args=[category.slug, gem.slug]),
                 reverse('add_gem'), reverse('login'), reverse('sign_up'),
                 reverse('search_results')]#, reverse('profile')

        # Create a list of pages to access
        templates = ['gems/index.html', 'gems/category.html', 'gems/gem.html',
                     'gems/add_gem.html', 'gems/login.html','gems/sign_up.html',
                     'gems/search_results.html']#, 'gems/search_results.html'

        # For each page in the page list, check if it extends from base template
        for template, page in zip(templates, pages):
            response = self.client.get(page)
            self.assertTemplateUsed(response, template)
            
    def test_url_reference_in_index_page_when_logged(self):
        # Create user and log in
        test_utils.create_user()
        self.client.login(username='testuser', password='test1234')

        # Access index page
        response = self.client.get(reverse('index'))

        # Check links that appear only for logged in user
        self.assertIn(reverse('add_gem'), response.content.decode('ascii'))
        self.assertIn(reverse('profile'), response.content.decode('ascii'))
        self.assertIn(reverse('logout'), response.content.decode('ascii'))
        
    def test_url_reference_in_index_page_when_not_logged(self):
        #Access index page with user not logged in
        response = self.client.get(reverse('index'))

        # Check links that appear only for user not logged in
        self.assertIn(reverse('login'), response.content.decode('ascii'))
        self.assertIn(reverse('sign_up'), response.content.decode('ascii'))
        
    def test_links_in_base_template(self):
        # Create a test category
        category = Category(name="Category 1")
        category.save()
        
        # Access index
        response = self.client.get(reverse('index'))

        # Check for URL referencing index
        self.assertIn(reverse('index'), response.content.decode('ascii'))
        self.assertIn(reverse('show_category', args=[category.slug]),
                      response.content.decode('ascii'))
        
    def test_gem_reference_in_category_page(self):
        # Create a test category
        category = Category(name="Category 1")
        category.save()
        
         # Create a test gem
        gem = Gem(category=category, name="Gem 1")
        gem.save()

        # Check for gem URL in category page
        response = self.client.get(reverse('show_category', args=[category.slug]))
        self.assertIn('href="' + gem.slug + '">' + gem.name.lower(),
                      response.content.decode('ascii').lower())
