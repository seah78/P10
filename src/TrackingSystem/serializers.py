from rest_framework import serializers
from TrackingSystem.models import User, Project

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        
    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "description", "project_type", "author")