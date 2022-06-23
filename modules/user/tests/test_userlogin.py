from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from faker import Faker
import json

from modules.user.models.usermodel import User


class UserTestView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()
        cls.email_address = cls.fake.email()
        cls.password = cls.fake.password()
        # cls.user_model = User.objects.create(email=cls.email_address, password=cls.password)
        cls.user_model = User.objects.create(email=cls.email_address, password=cls.password)
        cls.user_model.set_password(cls.password)
        cls.user_model.save()
        cls.url = '/api/v1/actuarial/users/login'
        cls.content = 'application/json'
        cls.user_auth = APIClient()
        cls.medium, cls.portal = 'Web', 'Actuarial'


    def test_wrong_pass(self):
        res = self.user_auth.post(self.url, data=json.dumps({"username": self.email_address, "password": self.fake.password() }), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 400)


    def test_wrong_email(self):
        res = self.user_auth.post(self.url, data=json.dumps({ "username": self.fake.email(), "password": self.password }), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 400)


    def test_auth(self):
        res = self.user_auth.post(self.url, data=json.dumps({ "username": self.email_address, "password": self.password }), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 200)
        

    def tearDown(self):
        return super().tearDown()