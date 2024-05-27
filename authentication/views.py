from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import CustomUser
from authentication.serializers import ListUserSerializer, BaseUserDetails


# Create your views here.
class UsersView(generics.ListAPIView):
    # this is only for testing purposes
    # it gets all users both drivers and customers
    queryset = CustomUser.objects.all()
    serializer_class = ListUserSerializer


class UserDetailsView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = BaseUserDetails
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
