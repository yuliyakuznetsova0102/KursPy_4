from django.urls import path
from .views import UserRegistrationView, UserLoginView, user_logout, UserPasswordResetView, UserPasswordResetDoneView, \
    UserPasswordResetConfirmView, UserPasswordResetCompleteView, ConfirmEmailView, ProfileUpdateView, BlockUserView, \
    ProfileView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('confirm-email/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('users/block/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
]
