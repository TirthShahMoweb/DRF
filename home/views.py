from django.contrib.auth import authenticate
from .models import Person
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, PeopleSerializer, RegisterSerializer

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

class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            # return Response({'status' : False, 'message' : serializer.errors}
            #                 , status = status.HTTP_400_BAD_REQUEST)
            raise Exception(serializer.errors)
        serializer.save()
        return Response({'status' : True, 'message' : 'User registered successfully'}
                        , status = status.HTTP_201_CREATED)
    

class PersonAPI(APIView):
    authentication_classes = [JWTAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        person = Person.objects.filter(color__isnull=False) 
        serializer = PeopleSerializer(person, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise Exception(serializer.errors)

    def put(self, request):
        data = request.data
        person = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise Exception(serializer.errors)

    def patch(self, request):
        data = request.data
        person = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(person, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise Exception(serializer.errors)

    def delete(self, request):
        data = request.data
        person = Person.objects.get(id=data['id'])
        person.delete()
        return Response({'message':"Person deleted"})

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

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        person = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(person, many=True)
        serializer_context = {
            'request' : (request)
            }
        context = serializer_context
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        person = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        person = Person.objects.get(id=data['id'])
        print(data, data['id'])
        serializer = PeopleSerializer(person, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    else:
        data = request.data
        person = Person.objects.get(id=data['id'])
        person.delete()
        return Response({'message':"Person deleted"})

@api_view(['POST'])
def login(request):

    if request.method=='POST':
        data=request.data
        serializer=LoginSerializer(data=data)

        if serializer.is_valid():
            data=serializer.validated_data
            return Response({"Message":"Success"})
        return Response(serializer.errors)

class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def create(self,request):
        """
            Creating the person
        """
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise Exception(serializer.errors)

    def list(self, request):
        """
            Listing the people and searching the people
        """
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        else:
            queryset = queryset.filter(color__isnull=False)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({ 'status' : 200 , 'data' : serializer.data}, status = status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
            Getting the person by id
        """
        person = Person.objects.get(id = pk)
        serializer = PeopleSerializer(person)
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    def update(self, request, pk=None):
        """
            Updating the person
        """
        data = request.data
        person = Person.objects.get(id = pk)
        serializer = PeopleSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise Exception(serializer.errors)

    def partial_update(self, request, pk=None):
        """
            Partially updating the person
        """
        data = request.data
        person = Person.objects.get(id = pk)
        serializer = PeopleSerializer(person, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise Exception(serializer.errors)

    def destroy(self, request, pk=None):
        """        
            Deleting the person
        """
        person = Person.objects.get(id = pk)
        person.delete()
        return Response({'message':"Person deleted"})