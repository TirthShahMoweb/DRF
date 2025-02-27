from django.urls import path, include

from .views import personViews, userViews, cityViews
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Generates access & refresh token
    TokenRefreshView      # Refreshes access token
)

router = DefaultRouter()
router.register(r'people', personViews.PeopleViewSet, basename='people')
urlpatterns = router.urls
urlpatterns = [

    path('',include(router.urls)),
    path('index/', userViews.index),
    path('loginAPI/', userViews.LoginAPI.as_view()),
    path('login/', userViews.login),
    path('signin/',userViews.SignInAPI.as_view()),
    path('register/', userViews.RegisterAPI.as_view()),

    path('person/', personViews.person),
    path('personApi/',personViews.PersonAPI.as_view()),

    # Pagination
    path('limitOffSetPagination/',personViews.detail_by_LimitOffSetPagination),
    path('pageNumberPagination/',personViews.detail_by_PageNumberPagination),
    path('cursorPagination/',personViews.PersonCursorAPI.as_view()),

    # Generic Views
    path('createPerson/',personViews.CreatePerson.as_view()),
    path('deletePerson/<int:pk>/',personViews.DeletePerson.as_view()),
    path('Listhobbycount/',personViews.ListAPIViewCount.as_view()),
    path('updatePerson/<int:pk>/',personViews.UpdatePerson.as_view()),
    path('retrievePerson/<int:pk>/',personViews.RetrievePerson.as_view()),
    path('personlistAPIView/',personViews.PersonListAPIView.as_view()),  

    path('listCreatePerson/',cityViews.ListCreatePerson.as_view()),
    
    path('retrieveDestroyPerson/<int:pk>/',personViews.RetrieveDestroyPerson.as_view()), 
    path('retrieveUpdatePerson/<int:pk>/',personViews.RetrieveUpdatePerson.as_view()), 
    path('retrieveUpdateDestroyPerson/<int:pk>/',personViews.RetrieveUpdateDestroyPerson.as_view()),

    # Token	
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]