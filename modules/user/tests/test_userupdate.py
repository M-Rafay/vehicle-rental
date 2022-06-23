from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from faker import Faker
import json
from backend import settings as SETTINGS

from modules.user.models.usermodel import User
from modules.user.models.customtokenmodel import CustomToken as Token


class UpdateUserTestView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()
        cls.password = cls.fake.password()
        cls.medium, cls.portal = 'Web', 'Actuarial'

        # Creating user and manager with their token
        manager_model = User.objects.create(email=cls.fake.email(), password=cls.password, role=SETTINGS.MANAGER_ROLE)
        cls.manager_token, manager_created = Token.objects.get_or_create(user=manager_model)
        user_model = User.objects.create(email=cls.fake.email(), password=cls.password)
        cls.user_id = user_model.id
        cls.user_token, user_created = Token.objects.get_or_create(user=user_model)
        cls.content = 'application/json'
        cls.url = '/api/v1/actuarial/users/update-user/'
        cls.update_user = APIClient()
        cls.user_obj = {
            "id": user_model.id,
            "role": SETTINGS.USER_ROLE,
            "full_name": "Testing user fullname",
            "phone_no": "0300",
            "is_active": True
        }
    
    def test_user_exists(self):
        self.assertTrue(User.objects.get(pk=self.user_id))

    def test_update_by_user_role(self):
        res = self.update_user.put(self.url, data=json.dumps(self.user_obj), HTTP_AUTHORIZATION='Token {}'.format(self.user_token), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 400)

    def test_update_user(self):
        res = self.update_user.put(self.url, data=json.dumps(self.user_obj), HTTP_AUTHORIZATION='Token {}'.format(self.manager_token), content_type=self.content, HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 200)


    def tearDown(self): return super().tearDown()