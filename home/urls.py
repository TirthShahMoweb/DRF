from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Generates access & refresh token
    TokenRefreshView      # Refreshes access token
)

router = DefaultRouter()
router.register(r'people', views.PeopleViewSet, basename='people')
urlpatterns = router.urls
urlpatterns = [

    path('',include(router.urls)),
    path('index/', views.index),
    path('loginAPI/', views.LoginAPI.as_view()),
    path('login/', views.login),
    path('person/', views.person),
    path('personApi/',views.PersonAPI.as_view()),
    path('signin/',views.SignInAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),

    # Pagination
    path('limitOffSetPagination/',views.detail_by_LimitOffSetPagination),
    path('pageNumberPagination/',views.detail_by_PageNumberPagination),
    path('cursorPagination/',views.PersonCursorAPI.as_view()),

    # Generic Views
    path('createPerson/',views.CreatePerson.as_view()),
    path('deletePerson/<int:pk>/',views.DeletePerson.as_view()),
    path('Listhobbycount/',views.ListAPIViewCount.as_view()),
    path('updatePerson/<int:pk>/',views.UpdatePerson.as_view()),
    path('retrievePerson/<int:pk>/',views.RetrievePerson.as_view()),

    path('listCreatePerson/',views.ListCreatePerson.as_view()),
    path('retrieveDestroyPerson/<int:pk>/',views.RetrieveDestroyPerson.as_view()), 
    path('retrieveUpdatePerson/<int:pk>/',views.RetrieveUpdatePerson.as_view()), 
    path('retrieveUpdateDestroyPerson/<int:pk>/',views.RetrieveUpdateDestroyPerson.as_view()),

    # Token	
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]