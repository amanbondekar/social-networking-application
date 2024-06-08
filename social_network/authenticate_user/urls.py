from django.urls import path
from .views import SignupView, LoginView,UserProfileAPI

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileAPI.as_view(), name='user_profile'),

]
