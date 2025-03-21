from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path
from .views import RegisterView, LoginView, LogoutView, DeleteAccountView, UserListView, GetUserByIDView, UpdateProfileUser, GetMe
from .auth_views import PasswordResetView, PasswordResetConfirmView
from .views import CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', GetMe.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('users/', UserListView.as_view(), name='users'),
    path('user/<int:user_id>/', GetUserByIDView.as_view(), name='get_user_by_id'),
    path('updateProfileUser/<int:user_id>/', UpdateProfileUser.as_view(), name='update_profile_user'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),


    # 

    path('reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
