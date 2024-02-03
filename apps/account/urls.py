from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.account import views

urlpatterns = [
    path('register/', views.RegistrationCustomerView.as_view()),
    path('activate/', views.ActivationEmailView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('change_password/', views.ChangePasswordView.as_view()),
    path('your_page/', views.UserView.as_view())
]

