from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import Users



class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] =  Users.objects.all()
        
        return context



class AboutView(TemplateView):
    template_name = 'main/about.html'
    


