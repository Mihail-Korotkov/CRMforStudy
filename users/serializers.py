from rest_framework import serializers
from users.models import Users,Tasks,Progress

class UserSerializer(serializers.ModelSerializer):

    tasks = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()
    complited_tasks = serializers.SerializerMethodField()


    class Meta:
        model = Users
        fields = ("username", "email", "role","tasks","total_tasks","complited_tasks")

    def get_tasks(self, obj):
        progress_list = Progress.objects.filter(user=obj).select_related('task')
        tasks = [p.task for p in progress_list]
        return TaskSerializer(tasks, many=True).data

    def get_total_tasks(self, obj):
        return Progress.objects.filter(user=obj).count()

    def get_complited_tasks(self, obj):
        return Progress.objects.filter(user=obj, task__status=True).count()
        



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ("title", "description", "created_at",)


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ("task", "user", "created_at",)




