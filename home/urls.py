from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Generates access & refresh token
    TokenRefreshView      # Refreshes access token
)

router = DefaultRouter()
router.register(r'people', views.PeopleViewSet, basename='people')
urlpatterns = router.urls
urlpatterns = [
    path('',include(router.urls)),
    path('register/', views.RegisterAPI.as_view()),
    path('loginAPI/', views.LoginAPI.as_view()),
    path('index/', views.index),
    path('login/', views.login),
    path('person/', views.person),
    path('personApi/',views.PersonAPI.as_view()),
    path('signin/',views.SignInAPI.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]