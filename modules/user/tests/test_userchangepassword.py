from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from faker import Faker
import json

from modules.user.models.usermodel import User
from modules.user.models.customtokenmodel import CustomToken as Token


class ChangePasswordTestView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        fake = Faker()
        # Creating user and generating token
        cls.password = fake.password()
        user_model = User.objects.create(email=fake.email())
        user_model.set_password(cls.password)
        user_model.save()
        cls.token, created = Token.objects.get_or_create(user=user_model)
        cls.content = 'application/json'
        cls.url = '/api/v1/actuarial/users/changepassword/'
        cls.change_pass = APIClient()
        cls.user_obj = { "old_password" : cls.password, "password1": "123456", "password2": "123456" }
    

    # If password1 and password2 doesnot matches
    def test_password_mismatch(self):
        res = self.change_pass.patch(self.url, data=json.dumps({ "old_password" : self.password, "password1": "123456", "password2": "1234567" }), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        self.assertEqual(res.status_code, 400)


    # New password cannot be same as old password
    def test_new_old_same_pass(self):
        res = self.change_pass.patch(self.url, data=json.dumps({ "old_password" : self.password, "password1": self.password, "password2": self.password }), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        self.assertEqual(res.status_code, 400)
    

    # Password length should be in between 6 - 20 characters
    def test_pass_length(self):
        res = self.change_pass.patch(self.url, data=json.dumps({ "old_password" : self.password, "password1": "12345", "password2": "12345" }), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        self.assertEqual(res.status_code, 400)
    

    # Verifying old password
    def test_wrong_old_pass(self):
        res = self.change_pass.patch(self.url, data=json.dumps({ "old_password" : "123456789", "password1": "123456", "password2": "123456" }), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        self.assertEqual(res.status_code, 400)


    # Test change password
    def test_change_password(self):
        res = self.change_pass.patch(self.url, data=json.dumps(self.user_obj), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        self.assertEqual(res.status_code, 200)


    # Test if token is deleted
    def test_token_deleted(self):
        self.change_pass.patch(self.url, data=json.dumps(self.user_obj), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        res = self.change_pass.patch(self.url, data=json.dumps(self.user_obj), HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content)
        self.assertEqual(res.status_code, 400)


    def tearDown(self): return super().tearDown()