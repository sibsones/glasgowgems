#from selenium.webdriver.common.keys import Keys
from gems.models import User, UserProfile #, Category, Gem, 

#===============================================================================
# Potentially useful helper methods for tests
#===============================================================================
#===============================================================================
# def login(self):
#     self.browser.get(self.live_server_url + '/admin/')
# 
#     # Types username and password
#     username_field = self.browser.find_element_by_name('username')
#     username_field.send_keys('admin')
# 
#     password_field = self.browser.find_element_by_name('password')
#     password_field.send_keys('admin')
#     password_field.send_keys(Keys.RETURN)
# 
# def user_login(self):
#     # Types username and password
#     username_field = self.browser.find_element_by_name('username')
#     username_field.send_keys('admin')
# 
#     password_field = self.browser.find_element_by_name('password')
#     password_field.send_keys('admin')
#     password_field.send_keys(Keys.RETURN)
#===============================================================================

#===============================================================================
# # Creates 10 test categories
# def create_categories():
#     # List of categories
#     categories = []
# 
#     # Create categories from 1 to 10
#     for i in range(1, 11):
#         cat = Category(name="Category " + str(i))
#         cat.save()
#         categories.append(cat)
# 
#     return categories
#===============================================================================

#===============================================================================
# def create_gems(categories):
#     # List of gems
#     gems = []
# 
#     # For each category create 2 gems
#     for i in range (0, len(categories)):
#         category = categories[i]
# 
#         # Name the gems according to the links and create a fake url
#         for j in range(0, 2):
#             gem_number = i * 2 + j + 1
#             gem = Gem(category=category, name="Gem " + str(gem_number))
#             gem.save()
#             gems.append(gem)
# 
#     return gems
#===============================================================================

# Creates a test user
def create_user():
    # Create a user
    user = User.objects.get_or_create(username="testuser", password="test1234",
                                      email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user, profile_image=None)[0]
    user_profile.save()

    return user, user_profile
