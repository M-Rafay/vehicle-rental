from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from faker import Faker
from backend import settings as SETTINGS

from modules.user.models.usermodel import User
from modules.user.models.customtokenmodel import CustomToken as Token


class UserDeleteView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()
        user_model = User.objects.create(email=cls.fake.email(), password=cls.fake.password(), role=SETTINGS.MANAGER_ROLE)
        cls.user_id = user_model.id
        user_model2 = User.objects.create(email=cls.fake.email(), password=cls.fake.password())
        cls.token, created = Token.objects.get_or_create(user=user_model)
        cls.token2, created2 = Token.objects.get_or_create(user=user_model2)
        cls.user_del = APIClient()
        cls.url = '/api/v1/actuarial/users/delete/?q='
        cls.medium, cls.portal = 'Web', 'Actuarial'

    def test_user_exists(self):
        self.assertTrue(User.objects.get(pk=self.user_id))
    
    def test_delete_user(self):
        user = User.objects.create(email=self.fake.email(), password=self.fake.password())
        res = self.user_del.delete(self.url + str(user.id), HTTP_AUTHORIZATION='Token {}'.format(self.token), HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_already_deleted_user(self):
        user = User.objects.create(email=self.fake.email(), password=self.fake.password())
        self.user_del.delete(self.url + str(user.id), HTTP_AUTHORIZATION='Token {}'.format(self.token), HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        res = self.user_del.delete(self.url + str(user.id), HTTP_AUTHORIZATION='Token {}'.format(self.token), HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 404)
    
    def test_delete_by_user_role(self):
        user = User.objects.create(email=self.fake.email(), password=self.fake.password())
        res = self.user_del.delete(self.url + str(user.id), HTTP_AUTHORIZATION='Token {}'.format(self.token2), HTTP_MEDIUM=self.medium, HTTP_PORTAL=self.portal)
        self.assertEqual(res.status_code, 400)


    def tearDown(self):
        return super().tearDown()