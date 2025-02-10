from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

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
]