from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
     path('forms/get/<int:id>', views.forms_get),
     path('forms/create', views.forms_post),
     path('forms/edit/<int:id>', views.forms_edit),
     path('forms/delete/<int:id>', views.forms_delete),
     path('answers/get/<int:id>', views.answers_get),
     path('answers/create/<int:id>', views.answers_post),
     path('answers/edit/<int:id>/<int:answer_id>', views.answers_edit),
     path('answers/delete/<int:id>/<int:answer_id>', views.answers_delete),
     path('users/create', views.users_create),
     path('users/get_all',views.user_get_all),
     path('about', views.about)
]
