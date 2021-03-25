from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from auth_rest_app.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django_rest_resetpassword.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets


@api_view(['GET', 'POST'])
def user_details(request):
    '''
        Get all user details and add new user
    '''
    # check request method
    if request.method == 'GET':
        user_obj = User.objects.all()
        user_serializer = UserSerializer(user_obj, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # User registration
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_login(request):
    '''
        verify user login details
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            user = User.objects.get(username=username)
            if user:
                login(request, user)
                token = Token.objects.create(user=user)
                print(token.key)
                return Response({'message': 'Login details verified',
                                 'token': token.key},
                                 status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid login details'},
                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'You are not a registered user'},
                status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_profile(request, pk):
    '''
        Update user profile details
    '''
    if request.method == 'PUT':
        user_obj = User.objects.filter(id=pk).update(
            username=request.POST['username'],
            password=make_password(
            request.POST['password']),
            profile_picture=request.FILES['profile_picture'],
            first_name=request.POST['first_name'])
        if user_obj:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(user_serializer.errors)


@api_view(['POST'])
def forgot_password(request):
    pass


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    # context = {
    #     'current_user': reset_password_token.user,
    #     'username': reset_password_token.user.username,
    #     'email': reset_password_token.user.email,
    #     'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    # }

    # # render email text
    # email_html_message = render_to_string('email/user_reset_password.html', context)
    # email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     "Password Reset for {title}".format(title="Some website title"),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "noreply@somehost.local",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.attach_alternative(email_html_message, "text/html")
    # msg.send()
    print('execute function')


class UserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class VerifyLogin(generics.GenericAPIView):
    """
    parameters:
    - name: username
      description: username 
      required: true
      type: string
      paramType: form
    - name: password
      paramType: form
      required: true
      type: string
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    username_param = openapi.Parameter('username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING)
    password_param = openapi.Parameter('password', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[username_param, password_param])
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.GET['username']
            password = request.GET['password']
            user = authenticate(username=username, password=password)
            try:
                user = User.objects.get(username=username)
                if user:
                    login(request, user)
                    return Response({'message': 'Login details verified'},
                                     status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid login details'},
                        status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({'error': 'You are not a registered user'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
