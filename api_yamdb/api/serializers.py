from datetime import date

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


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

        user = get_object_or_404(User, username=username)

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
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}.'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = (
            'author',
            'pub_date'
        )

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')

            if Review.objects.filter(
                title_id=title_id,
                author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Отзыв уже оставлен.'
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = (
            'author',
            'pub_date'
        )
