from django.urls import path

from authenticate.views import CheckPasswordTokenAPIView, LoginAPIView, RegisterAPIView, EmailVerifyAPIView, RequestEmailPasswordResetAPIView, SetNewPasswordAPIView, UserProfileUpdateAPIView, ViewUsersAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name='register'),
    path("update/", UserProfileUpdateAPIView.as_view(), name='update'),
    path("email-verify/", EmailVerifyAPIView.as_view(), name='email-verify'),
    path("login/", LoginAPIView.as_view(), name='login'),
    path('request-reset-email/', RequestEmailPasswordResetAPIView.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', CheckPasswordTokenAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-confirm'),
    path('users/', ViewUsersAPIView.as_view(), name='users'),


    # path('password-reset/', ResetPassword.as_view(), name='password-reset'),
]