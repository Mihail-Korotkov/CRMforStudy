from rest_framework import serializers
from users.models import Users,Tasks,Progress

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("username", "email", "role")



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ("title", "description", "created_at",)


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ("task", "user", "created_at",)


