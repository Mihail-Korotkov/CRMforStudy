from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import Users, Tasks
from main.utils import get_activity_percentage, get_avarege_progress
from django.db.models import F, Q, Case, Count, ExpressionWrapper, FloatField, IntegerField, Value, When
from django.db.models.functions import Cast






class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['tasks_done'] = Tasks.objects.filter(status = True)
        context['tasks_done_percent'] = get_avarege_progress()
        context['activity_percent'] = get_activity_percentage()

        users = Users.objects.annotate(
            total_tasks=Count('progress'),
            completed_tasks=Count('progress', filter=Q(progress__task__status=True)),
            progress_percent=Case(
                        When(total_tasks=0, then=Value(0)),
                        default=ExpressionWrapper(
                            Cast(F('completed_tasks'), FloatField()) / 
                            Cast(F('total_tasks'), FloatField()) * 100,
                            output_field=IntegerField()
                        )
                    )
                )
        
        
        context['users'] = users
        

        
        return context



class AboutView(TemplateView):
    template_name = 'main/about.html'
    


