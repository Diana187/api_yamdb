from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Review, Comment, Genre
from users.models import User


class ValidateUsernameEmailMixin:
    """Миксин проверки email и корректного имени пользователя.
    """
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует.'
            )

        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Запрещено использовать "me" в качестве имени пользователя'
            )

        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = User


class SignupSerializer(serializers.ModelSerializer, ValidateUsernameEmailMixin):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    # confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username',)


class UserSerializer(serializers.ModelSerializer, ValidateUsernameEmailMixin):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Category."""
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ('name', 'slug')
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('name', 'slug')
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Genre."""
    slug = serializers.SlugField()

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=('name', 'slug')
            )
        ]

#class ReviewRecursiveSerialaizer(serializers.Serializer):

    #def to_representation(self, value):
        #serializer = Review(value, context=self.context)
        #return serializer.data

# class TitleSerializerDetail(serializers.ModelSerializer):
#     genre = GenreSerializer(many=True, required=False)
#     category = CategorySerializer()
#     # permission_classes = (IsAdminOrReadOnly,)
#
#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'rating',
#                   'description', 'genre', 'category')
#
#     def create(self, validated_data):
#         genres = validated_data.pop('genre')
#         title = Title.objects.create(**validated_data)
#
#         for genre in genres:
#             current_genre, status = Genre.objects.get_or_create(**genre)
#             title.objects.add(genre=current_genre)
#         return title


#class FilterReviewListSerializer(serializers.ListSerializer):
    #def to_representation(self, data):
       # data = data.filter(title=None)
        #return super().to_representation(data)


#class CommentRecursiveSerialaizer(serializers.Serializer):

    #def to_representation(self, value):
        #serializer = CommentSerializer(value, context=self.context)
        #return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Review."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    comment = CommentSerializer(many=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score',
                  'pub_date', 'comment')
        read_only_fields = ('author',)
        model = Review

    def validate(self, data):
        if self.context['request'] != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
            author=author,
            title=title_id
        ).exists():
            raise ValidationError(
                'Отзыв к произведению уже написан.'
            )
        return data


class TitleSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Titles."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    # permission_classes = (IsAdminOrReadOnly,)

    rating = serializers.SerializerMethodField()
    review = ReviewSerializer(many=True)
    # rating = Title.objects.annotate(rating=Avg("reviews__score"))
    # queryset = Title.objects.all()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category', 'review')


    def get_queryset(self):
        queryset = Title.objects.annotate(
            rating=Avg("reviews__score"))
        return queryset


# class TitleSerializerDetail(serializers.ModelSerializer):
#     genre = GenreSerializer(many=True, required=False)
#     category = CategorySerializer()
#     # permission_classes = (IsAdminOrReadOnly,)
#
#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'rating',
#                   'description', 'genre', 'category')
#
#     def create(self, validated_data):
#         genres = validated_data.pop('genre')
#         title = Title.objects.create(**validated_data)
#
#         for genre in genres:
#             current_genre, status = Genre.objects.get_or_create(**genre)
#             title.objects.add(genre=current_genre)
#         return title
