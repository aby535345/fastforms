from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
     #curl -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:8000/api/token/
     path('forms/<int:id>', views.forms),
     path('answers/<int:id>', views.answers),
     path('users/create', views.users_create),
     path('users/get_all',views.user_get_all),
]