# Every backend has a special requirement after registraion and login.
# The hook is a way to add this requirement to the backend.

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .models import AuthUser
from .serializers import UserSerializer
from researchs.models import Researchers

def post_registration_hook(request: Request, serializer: UserSerializer):
    """
    This function is called after a user registers.
    """
    r = Researchers(id=serializer.data['id'])
    r.save()
    del serializer.data['id']
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def post_login_hook(request: Request, serializer: UserSerializer):
    """
    This function is called after a user logs in.
    """
    try:
        Researchers.objects.get(id=serializer.data['id'])
    except Researchers.DoesNotExist:
        return Response(data={'error':['A user with this username and password was not found.']}, status=status.HTTP_400_BAD_REQUEST)
    
    del serializer.data['id']
    return Response(serializer.data, status=status.HTTP_200_OK)


def check_user(user: AuthUser):
    """
    This function is called after a user logs in.
    """
    try:
        Researchers.objects.get(id=user.id)
    except Researchers.DoesNotExist:
        return False
    return True