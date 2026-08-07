from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegistrationForm


# Create your views here.
class UserProfileView(TemplateView):
    template_name = 'users/profile.html'



class UserCabinetView(TemplateView):
    template_name = 'users/cabinet.html'







class UserRegistrationView(SuccessMessageMixin, CreateView):

    
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')
    failure_url = 'users:registration'
    success_message = 'Вы успешно зарегистрировались'
    failure_message = 'Неверные данные'


    





class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = 'main:index'
    failure_url = 'user:login'
    form_class = UserLoginForm
    success_message = 'Вы успешно вошли в аккаунт'
    failure_message = 'Неверный логин или пароль'
    



