from rest_framework.authentication import TokenAuthentication
from modules.user.models.customtokenmodel import CustomToken

class customtoken(TokenAuthentication):
    model = CustomToken

