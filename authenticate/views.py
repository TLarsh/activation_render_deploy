from django.shortcuts import render
from authenticate.serializers import EmailVerifySerializer, LoginSerializer, RegisterSerializer, RequestEmailPasswordResetSerializer, SetNewPasswordSerializer, UserProfileUpdateSerializer, UserSerializer
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
# Create your views here.


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user = User.objects.get(email=user_data['email'])
        # print(user)
        token = RefreshToken.for_user(user).access_token 
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        url = 'http://'+current_site+relative_link+"?token="+str(token)
        emailBody = 'Hi '+user.username+", please activate your email using the link below"
        data = {'email_body':emailBody, 'send_to':user.email,  'activation_link':url}
        return Response(data)

class EmailVerifyAPIView(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer
    token_param_config=openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )
    @swagger_auto_schema(manual_parameters=[token_param_config])    
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email":"Email successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error":"Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class RequestEmailPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = RequestEmailPasswordResetSerializer
    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            absurl = 'http://' + current_site + relative_link
            email_body = 'Hello, \n Use the link to reset your password'
            data = {'email_body':email_body, 'to_email':user.email, 'email_subject': 'Reset your password'}
        return Response({'success': absurl}, status = status.HTTP_200_OK)
    
    
    
class CheckPasswordTokenAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id =smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Invalid token, please request new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'Credentials Valid', 'uidb64':uidb64, 'token':token, 'user':user.email}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token is Invalid, please request new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password reset successful'})

        
class ViewUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class UserProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = (permissions.AllowAny,)
    