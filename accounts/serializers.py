from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, password_validation


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_validation.validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
