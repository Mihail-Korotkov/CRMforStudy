from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import Users, Tasks
from main.utils import get_activity_percentage, get_avarege_progress






class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] =  Users.objects.all()
        context['tasks_done'] = Tasks.objects.filter(status = True)
        context['tasks_done_percent'] = get_avarege_progress()
        context['activity_percent'] = get_activity_percentage()


        
        return context



class AboutView(TemplateView):
    template_name = 'main/about.html'
    


