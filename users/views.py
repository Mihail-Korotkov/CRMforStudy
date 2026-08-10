from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from django.contrib.auth import update_session_auth_hash
from django.contrib import messages



from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateProfileForm


from users.models import Users


# Create your views here.
class UserProfileView(TemplateView):
    template_name = "users/profile.html"
    # form_class = ProfileForm


class UserProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserUpdateProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль был успешно обновлен.")
            return redirect('users:cabinet')
        else:
            # Сохраняем ошибки в сессии
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('users:cabinet')
    
    def get(self, request, *args, **kwargs):
        return redirect('users:cabinet')


class UserCabinetView(TemplateView):
    template_name = "users/cabinet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем форму профиля с данными текущего пользователя
        context['form'] = UserUpdateProfileForm(instance=self.request.user)
        return context

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

    


class UserRegistrationView(SuccessMessageMixin, CreateView):

    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")
    failure_url = "users:registration"
    success_message = "Вы успешно зарегистрировались"
    failure_message = "Неверные данные"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("main:index")
    failure_url = "user:login"
    form_class = UserLoginForm
    success_message = "Вы успешно вошли в аккаунт"
    failure_message = "Неверный логин или пароль"


class UserListView(ListView):
    model = Users  # Указываем модель, данные которой нужно вывести
    template_name = "users/users_list.html"  # Путь к вашему шаблону
    context_object_name = (
        "users"  # Имя переменной в шаблоне (по умолчанию 'object_list')
    )
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Users.objects.count()
        return context

    # Количество объектов на странице


# views.py - Минимальный код!
class UserPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("users:cabinet")
    # form_class не указываем - используем PasswordChangeForm

    def get(self, request, *args, **kwargs):
        return redirect("users:cabinet")

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect('users:cabinet')

