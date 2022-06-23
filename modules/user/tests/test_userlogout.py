from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from faker import Faker
import json
from backend import settings as SETTINGS

from modules.user.models.usermodel import User
from modules.user.models.customtokenmodel import CustomToken as Token


class CreateUserTestView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()
        cls.email_address = cls.fake.email()
        cls.password = cls.fake.password()
        cls.manager_role = SETTINGS.MANAGER_ROLE
        cls.user_role = SETTINGS.USER_ROLE
        cls.medium, cls.portal = 'Web', 'Actuarial'

        # Creating user and generating token
        user_model = User.objects.create(email=cls.fake.email(), password=cls.password, role=cls.manager_role)
        cls.token, created = Token.objects.get_or_create(user=user_model)
        cls.content = 'application/json'
        cls.url = '/api/v1/actuarial/users/logout/'
        cls.logout_user = APIClient()
    
    def test_logout_user(self):
        res = self.logout_user.post(self.url, HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 200)
    
    def test_logout_user_wrong_token(self):
        res = self.logout_user.post(self.url, HTTP_AUTHORIZATION='Token {}'.format(str(self.token)+"asdf"), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 401)

    def tearDown(self): return super().tearDown()