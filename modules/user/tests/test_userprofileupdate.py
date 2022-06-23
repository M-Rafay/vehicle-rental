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
        fake = Faker()
        user_model = User.objects.create(email=fake.email(), password=fake.password())
        cls.user_token, user_created = Token.objects.get_or_create(user=user_model)
        cls.user_id = user_model.id
        cls.content = 'application/json'
        cls.url = '/api/v1/actuarial/users/update-profile/'
        cls.update_user = APIClient()
        cls.user_obj = {
            "full_name": fake.name(),
            "phone_no": "0300",
        }

    def test_user_exists(self):
        self.assertTrue(User.objects.get(pk=self.user_id))
    

    def test_update_user(self):
        res = self.update_user.patch(self.url, data=json.dumps(self.user_obj), HTTP_AUTHORIZATION='Token {}'.format(self.user_token), content_type=self.content)
        self.assertEqual(res.status_code, 200)

    def tearDown(self): return super().tearDown()