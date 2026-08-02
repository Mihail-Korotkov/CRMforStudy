from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class UserProfileView(TemplateView):
    template_name = 'users/profile.html'
