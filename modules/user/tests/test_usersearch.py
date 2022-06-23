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
        cls.user_model = User.objects.create(email=cls.fake.email(), password=cls.password, role=cls.manager_role)
        cls.token, created = Token.objects.get_or_create(user=cls.user_model)
        for i in range(5):
            is_active = False
            if i % 2 == 0:
                is_active = True
            User.objects.create(email=cls.fake.email(), password=cls.password, role=cls.user_role, is_active=is_active)
        cls.content = 'application/json'
        cls.url = '/api/v1/actuarial/users/'
        cls.list_user = APIClient()
    def test_user_exists(self):
        self.assertTrue(User.objects.get(pk=self.user_model.id))

    def test_list_user(self):
        res = self.list_user.get(self.url, HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 200)
    
    def test_list_user_inactive(self):
        res = self.list_user.get(self.url+"?list=inactive", HTTP_AUTHORIZATION='Token {}'.format(self.token), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 200)

    def tearDown(self): return super().tearDown()