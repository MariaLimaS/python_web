from django.conf import settings
import jwt
from rest_framework import permissions
from.models import UserModel

class IsNotSuspendend(permissions.BasePermission):

    def has_permission(self,request,view):

        user= request.user
        return not user.suspenso

def validated_token (token):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = UserModel.objects.filter(id=payload['user_id']).first()

        if not user:
            return False

        user.refresh_from_db()
        return user

    except Exception as e :
        return False

class ValidToken(permissions.BasePermission):

    def has_permission(self, request, view):

        token = request.headers.get('token')
        user = validated_token(token)

        if not user:
            return False
            
        request.user = user

        return True

class ValidAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("token")
        payload =jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])

        try:
            user = UserModel.objects.get(id=payload['user_id'], tipo='root')

            if not user:
                return False

            request.user = user
            return True
        
        except Exception as e:
            return False 
        
