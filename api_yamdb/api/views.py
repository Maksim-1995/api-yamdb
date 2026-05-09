from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
    UserMeSerializer
)
from .permissions import IsAdmin


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    user, _ = User.objects.get_or_create(
        username=username,
        email=email,
    )

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject='YaMDb. Код подтверждения.',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {
            'email': email,
            'username': username,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def api_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token = AccessToken.for_user(user)

    return Response(
        {
            'token': str(token),
        },
        status=status.HTTP_200_OK,
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def api_me(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data)

        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
