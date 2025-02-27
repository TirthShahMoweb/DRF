from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from ..serializers.userSerializers import RegisterSerializer, LoginSerializer



class LoginAPI(APIView):
    """
        Login API using Token based Authentication
    """

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            # return Response({'status' : False , 'message' : serializer.errors}
            #                 , status = status.HTTP_400_BAD_REQUEST)
            raise Exception(serializer.errors)

        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            # return Response({'status' : False, 'message' : 'Invalid credentials'}
            #                 , status = status.HTTP_400_BAD_REQUEST)
            raise Exception(serializer.errors)

        token , _ = Token.objects.get_or_create(user = user) # Get or create token for the user and _ is for the True or False.
        return Response({'status' : True, 'message' : 'User logged in successfully', 'token' : token[0].key}
                    , status = status.HTTP_200_OK)

class SignInAPI(APIView):
    '''
        Sign In API for JWT Authentication
    '''
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            raise Exception(serializer.errors)

        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            raise Exception(serializer.errors)

        refresh = RefreshToken.for_user(user)

        return Response( {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

@api_view(['POST'])
def login(request):

    if request.method=='POST':
        data=request.data
        serializer=LoginSerializer(data=data)

        if serializer.is_valid():
            data=serializer.validated_data
            return Response({"Message":"Success"})
        return Response(serializer.errors)

class RegisterAPI(APIView):
    '''
        Register API
    '''
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            raise Exception(serializer.errors)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
def index(request):
    if request.method == 'GET':

        json_response = {
        'name' : 'Scaler',
        'courses' : ['C++', 'Python'],
        'method' : 'GET'}
        # print(request.GET.get("search"))
    else:
        json_response = {
        'name' : 'Scaler',
        'courses' : ['C++', 'Python'],
        'method' : 'Post'}
        data = request.data
    return Response(json_response)