from rest_framework import status, generics
from authentication.models import CustomUser
from authentication.serializers import ListUserSerializer


# Create your views here.
class UsersView(generics.ListAPIView):
    # this is only for testing purposes
    # it gets all users both drivers and customers
    queryset = CustomUser.objects.all()
    serializer_class = ListUserSerializer
