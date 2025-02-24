from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.db.models import Count, Max,Sum ,Subquery, OuterRef, Avg
from django_filters.rest_framework import DjangoFilterBackend

from .filters import PersonFilter

from .models import Person, City, Hobby

from rest_framework import viewsets, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import LoginSerializer, PeopleSerializer, RegisterSerializer, CitySerializer

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

class PersonAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
            Get the list of people by applying Manual pagination
        '''
        person = Person.objects.select_related('city', 'color').prefetch_related('hobbies').filter(color__isnull=False) 
        try:
            page = request.GET.get('page', 1)
            page_size = 3
            paginator = Paginator(person, page_size)
            person = paginator.page(page)
            serializer = PeopleSerializer(person, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"status":"False",'message':'Invalid Page'})

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

class CustomPagination(PageNumberPagination):
    page_size = 3  # Number of items per page
    page_size_query_param = 'page_size'  # Allows dynamic page size via query param
    max_page_size = 100  # Prevents excessive page sizes

@api_view(['GET'])
def detail_by_PageNumberPagination(request):
    '''
        Get the list of people by applying PageNumberPagination
    '''
    if request.method == 'GET':
        person = Person.objects.filter(color__isnull=False).order_by('id')
        paginator = CustomPagination()
        person = paginator.paginate_queryset(person, request)
        serializer = PeopleSerializer(person, many=True)
        return paginator.get_paginated_response(serializer.data)

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3  # Default number of records per page
    max_limit = 100  # Prevents large data requests
    offset_query_param = 'skip'

@api_view(['GET'])
def detail_by_LimitOffSetPagination(request):
    '''
        Get the list of people by applying LimitOffsetPagination
    '''
    if request.method == 'GET':
        person = Person.objects.filter(color__isnull=False)
        paginator = CustomLimitOffsetPagination()
        person = paginator.paginate_queryset(person, request)
        serializer = PeopleSerializer(person, many=True)
        return paginator.get_paginated_response(serializer.data)

class CustomCursorPagination(CursorPagination):
    page_size = 3  # Number of records per page
    ordering = 'id'  # Field used for ordering results (must be indexed for efficiency)

class PersonCursorAPI(APIView):
    def get(self, request):
        '''
            Get the list of people by applying CursorPagination
        '''
        person = Person.objects.all().order_by('id')  
        paginator = CustomCursorPagination()
        person = paginator.paginate_queryset(person, request, view=self)
        serializer = PeopleSerializer(person, many=True)
        return paginator.get_paginated_response(serializer.data)

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
        # print(data, data['id'])
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

    @action(detail=False, methods=['GET'])
    def details(self, request):
        """
            Sending the welcome message
        """
        return Response({'message' : 'Welcome message sent'}) 

    @action(detail=True, methods=['GET'])
    def welcome_message_person(self, request, pk=None):
        """
            Sending the welcome message to the person
        """ 
        return Response({'message' : f'Welcome message sent to person with id {pk}'})    

class ListAPIViewCount(ListAPIView):
    '''
        List of people
    '''
    # avg_hobby_count = Person.objects.annotate(hobby_count=Count('hobbies')).aggregate(Avg('hobby_count'))['hobby_count__avg']
    serializer_class = PeopleSerializer
    queryset = Person.objects.annotate(hobby_count=Count('hobbies'))
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = PersonFilter
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'age']

    def get_queryset(self):
        queryset = self.queryset
        city_name = self.request.query_params.get('city', None) 
        if city_name:
            queryset = queryset.filter(city__name=city_name)
        return queryset

class CreatePerson(CreateAPIView):
    '''
        Create person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

class DeletePerson(DestroyAPIView):
    '''
        Delete person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

class RetrievePerson(RetrieveAPIView):
    '''
        Retrieve person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

class UpdatePerson(UpdateAPIView):
    '''
        Update person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

class ListCreatePerson(ListCreateAPIView):
    '''
        Create or List person
    '''
    serializer_class = CitySerializer
    queryset = City.objects.prefetch_related('city_person') \
    .annotate(max_age=Max('city_person__age')) \
    .filter(max_age__isnull=False)
    
    # queryset = City.objects.annotate(max_age=Max('city_person__age')).filter(max_age__isnull=False)
    # queryset = City.objects.annotate(max_age=Count('city_person')).filter(max_age__gt=0).order_by('max_age')

class RetrieveUpdatePerson(RetrieveUpdateAPIView):
    '''
        Retrieve or Update person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

class RetrieveDestroyPerson(RetrieveDestroyAPIView):
    '''
        Retrieve or Destroy person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

class RetrieveUpdateDestroyPerson(RetrieveUpdateDestroyAPIView):
    '''
        Retrieve, Update or Destroy person
    '''
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()