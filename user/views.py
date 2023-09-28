from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.hashers import make_password
from .middlewares import Middlewares
from .serializers import UserSerializers, UserUpdateSerializer, CustomTokenSerializer, UserListSerializer
from .models import UserModel
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .permissions import ValidToken, ValidAdmin
import jwt
from django.conf import settings
from uuid import UUID
from rest_framework.response import Response


class CreatUserView (generics.CreateAPIView):
    model=UserModel
    serializer_class = UserSerializers

class CustomTokenView(TokenObtainPairView):
    serializer_class= CustomTokenSerializer

class LogoutView(APIView):
    permission_classes=[ValidToken]

    def post (self, request):
        refresh= request.data.get('refresh_token')

        if refresh:

            try:
                token = RefreshToken(refresh)
                token.blacklist()
                return Response({"detail": "Logout realizado com sucesso!"}, status=200)
            except  Exception as e:
                return Response({"detail": "Erro ao realizar o logout!"}, status=400)

        return Response({"detail":"O token não foi enviado!"}, status=400)

class UserViewPrivate (APIView):
    permission_classes = [ValidToken]
    queryset = UserModel.objects.all()

    def get_queryset(self,pk):
        try:
            return self.queryset.get(pk=pk)
        except UserModel.DoesNotExist:
            raise Http404

    def put(self,request):
        user_id = Middlewares.decode(request.headers)
        tipo = self.get_queryset(user_id)

        #data = UserSerializers(tipo).data
        user = tipo
        data = request.data

        try:
            if(data["password"] and user.check_password(data["password_back"])):
                user.set_password(make_password(data["password"]))
                data["password"] = make_password(data["password"])
        except:
            data["password"]=user.password
        
        serializer = UserUpdateSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Atualizado com sucesso!"}, status=200)

        return Response(serializer.errors, status=400)

class AdminView(APIView):

    permission_classes =[ValidToken, ValidAdmin]
    queryset=UserModel.objects.all()

    def get_queryset(self, pk,tipo):

        try:
            return self.queryset.get(pk=pk, tipo=tipo)

        except UserModel.DoesNotExist:
            return Http404
    
    def get(self, request, id=None):

        if id is not None:
            user = self.get_queryset(id, tipo='client')
            serializers= UserSerializers(user)

        else:
            users=self.queryset.filter(tipo='client')
            serializers= UserListSerializer(users, many=True)
        
        return Response(serializers.data, status=200)
    
    def patch(self, request, id):

        user=self.get_queryset(id, tipo='client')
        serializers= UserSerializers(user, data=request.data, partial=True)

        if serializers.is_valid():

            serializers.save()
            serializers=UserListSerializer(serializers.data)

            return Response(serializers.data, status=201)
        
        return Response(serializers.errors, status=400)