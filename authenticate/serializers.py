from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib import auth
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
        # account_number = User.acc_no
        
        # if not account_number:
        #     generator = str(self.id).zfill(7)
        #     self.account_number = f'013{generator}'

        if not username.isalnum():
            raise serializers.ValidationError('username must only contain alphanumeric')
        return attrs
    
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=3, max_length=500)
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 225, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']
        
    def validate(self, attrs):
        email =  attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account dissabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email not verified")
        return{
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens
        }
        
class RequestEmailPasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=9)
    class Meta:
        model = User
        fields = ['email']
        
    
class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=50, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']
        
        def validate(self, attrs):
            try:
                password = attrs.get('password')
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')
                id = force_str(urlsafe_base64_decode
                               (uidb64))
                user = User.objects.get(id=id)
                # print(password)
                # print (user)
                if not PasswordResetTokenGenerator.check_token(user, token):
                    raise AuthenticationFailed('The reset link is invalid', 401)
                
                user.set_password(password)
                user.save()
            except Exception as e:
                raise AuthenticationFailed('The reset link is invalid', 401)
            return super().validate(attrs)
        
        
            
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'account_number', 'balance']
        
        



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    # delete_image = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'current_password',
            'password',
            # 'phone_number',
            # 'lastname',
            # 'fullname',
            # 'image',
            # 'delete_image'
        )
        
        
    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        current_password = attrs.get('current_password')

        if current_password and not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect.")

        return attrs

    def update(self, instance, validated_data):
        # user = self.context[request].user
        email = validated_data.get('email', instance.email)
        username = validated_data.get('username', instance.username)
        password = validated_data.get('password', instance.password)
        # fullname = validated_data.get('fullname', instance.fullname)
        # lastname = validated_data.get('lastname', instance.lastname)
        # phone_number = validated_data.get('phone_number', instance.phone_number)
        # image = validated_data.get('bio', instance.image)
        # delete_image = validated_data.get('delete_image', False)



        if email is not None:
            instance.email=email
        if username is not None:
            instance.username = username
        # if fullname is not None:
        #     instance.fullname = fullname
        # if lastname is not None:
        #     instance.lastname = lastname
        # if phone_number is not None:
        #     instance.phone_number = phone_number  
        # if image is not None:
        #     instance.image = image
        # if delete_image:
        #    instance.delete_image = None
        #    instance.image.delete(save=False)
            
        new_password = password
        if new_password:
            instance.set_password(new_password)
         
        instance.save()
        return instance