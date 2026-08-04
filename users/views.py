from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class UserProfileView(TemplateView):
    template_name = 'users/profile.html'



class UserCabinetView(TemplateView):
    template_name = 'users/cabinet.html'







class UserRegistrationView(TemplateView):
    template_name = 'users/registration.html'
    





class UserLoginView(TemplateView):
    template_name = 'users/login.html'



