from rest_framework import serializers
from TrackingSystem.models import Contributors, User, Project, Issues, Comments


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

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


class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ("id", "user", "project", "role")


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = (
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "project",
            "status",
            "author",
            "assigned_user",
        )


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "description", "author_user_id", "issue_id")
