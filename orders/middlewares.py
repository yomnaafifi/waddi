from rest_framework_simplejwt.tokens import AccessToken as Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from customer.models import Customer
from driver.models import Driver

CustomUser = get_user_model()


@database_sync_to_async
def returnUser(token_string):
    try:
        token_dict = Token(token_string)
        user = CustomUser.objects.get(id=token_dict["user_id"])
        print(user.is_customer, "::::::::::::::::::::::::::::::")
        if user.is_customer:
            user = Customer.objects.get(user=user)
        elif user.is_driver:
            user = Driver.objects.get(user=user)
        else:
            user = AnonymousUser()
    except Exception as e:
        print(e)
        user = AnonymousUser()

    return user


class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict["token"][0]
        user = await returnUser(token)
        scope["user"] = user
        return await self.app(scope, receive, send)
