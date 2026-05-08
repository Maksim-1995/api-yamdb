from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}.'
            )
        return value

    def validate(self, data):
        username = data['username']
        email = data['email']

        existed_username = User.objects.filter(username=username).first()
        existed_email = User.objects.filter(email=email).first()

        if existed_username and existed_username.email != email:
            raise serializers.ValidationError(
                f'Пользователь с именем {username} уже существует.'
            )

        if existed_email and existed_email.username != username:
            raise serializers.ValidationError(
                f'Пользователь с почтой {email} уже существует.'
            )

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f'Пользователь {username} не найден.'
            )

        if not default_token_generator.check_token(
            user,
            confirmation_code,
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}.'
            )
        return value


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}.'
            )
        return value
