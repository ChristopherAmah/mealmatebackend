# from rest_framework import serializers
# from .models import User
# from django.contrib.auth import authenticate


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['full_name', 'email', 'password']

#     def create(self, validated_data):
#         return User.objects.create_user(
#             full_name=validated_data.get('full_name'),
#             email=validated_data['email'],
#             password=validated_data['password']
#         )


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(email=data['email'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Invalid email or password")
#         return user


from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            full_name=validated_data.get('full_name'),
            email=validated_data['email'],
            password=validated_data['password']
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        # Return a dictionary with 'user' key so views can access it consistently
        return {'user': user}
