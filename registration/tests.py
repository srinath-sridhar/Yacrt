from django.test import TestCase
from django.contrib.auth.models import User

class RegistrationAppViewTests(TestCase):

    #Simple test to see if correct view was rendered
    def test_signin_form_rendered(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find("Please Sign In")!=-1)

    #set up for tests
    def setup_user(self,active):
        test_user = User.objects.create(username="testuser",first_name="test",last_name="test",email="test@test.com",is_active=active)
        test_user.set_password("test")
        test_user.save()

    #tests if a valid user can login
    def test_valid_user_can_signin(self):
        self.setup_user(True)
        response = self.client.post("/registration/authenticate_user/",{'username':'testuser','password':'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find("User authenticated")!=-1)
  
    #tests to make sure that invalid user cannot login
    def test_invalid_user_cannot_signin(self):
        self.setup_user(True)
        response = self.client.post("/registration/authenticate_user/",{'username':'t','password':'t'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find("User invalid")!=-1)

    #tests to make sure that invalid user cannot login
    def test_inactive_user_cannot_signin(self):
        self.setup_user(False)
        response = self.client.post("/registration/authenticate_user/",{'username':'testuser','password':'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find("User account disabled")!=-1)
