from django.contrib import auth
from django.shortcuts import get_list_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
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


from users.models import Progress, Tasks, Users
from users.utils import q_search



# Create your views here.
class UserDetailView(DetailView):
    model = Users
    template_name = "users/profile.html"
    context_object_name = "profile_user"
    pk_url_kwarg = "user_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        user_progress = Progress.objects.filter(user=user)
        completed_tasks = user_progress.filter(task__status=True)

        context['completed_tasks_count'] = completed_tasks.count()
        context['total_tasks_count'] = user_progress.count()
        context['user_tasks'] = [p.task for p in user_progress][:5]

        total = user_progress.count()
        if total > 0:
            context['user_progress'] = int((completed_tasks.count() / total) * 100)
        else:
            context['user_progress'] = 0
            
        context['activity_percentage'] = 94  # Здесь можно добавить реальный расчет
        
        return context





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
        context['user_tasks'] = Progress.objects.filter(
            user=self.request.user
        ).select_related('task').order_by('-created_at')

        context['tasks_done'] = Progress.objects.filter(
            user=self.request.user,
            task__status=True
        ).count()


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

    def get_queryset(self):
        role_filter = self.request.GET.get("role")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get('q')

        users = Users.objects.all()
 
        if query:
            users = q_search(query)
        else:
            users = Users.objects.all()

        # if on_sale:
        #     goods =  goods.filter(discount__gt=0)

        # if order_by and order_by !=  "default":  
        #     goods= goods.order_by(order_by)
        

        return users

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
@login_required
def add_task_simple(request):
    if request.method == 'POST':
        task_title = request.POST.get('task_title','').strip()
        if task_title:
            task,created = Tasks.objects.get_or_create(
                title = task_title,
                defaults = {'description':f'Задача:{task_title}'}
            )
            if not Progress.objects.filter(user=request.user, task=task).exists():
                Progress.objects.create(user= request.user, task = task)
                messages.success(request,f'Задача"{task_title}" добавлена!')
            else:
                messages.warning(request,"эта задача уже у вас в списке")
        else:
            messages.error(request,"Название задачи не может быть пустым")
    return redirect('users:cabinet')


@login_required
def delete_task_simple(request, task_id):
    try:
        progress = Progress.objects.get(user = request.user, task_id = task_id)
        progress.delete()
        messages.success(request,"Задача удалена")
    except Progress.DoesNotExist:
        messages.error(request,"Задача не найдена")
        
    return redirect('users:cabinet')

@login_required
def toggle_task_simple(request, task_id):
    """Переключение статуса задачи (выполнена/не выполнена)"""
    try:
        progress = Progress.objects.get(user=request.user, task_id=task_id)
        task = progress.task
        task.status = not task.status
        task.save()
        
        status_text = 'выполнена' if task.status else 'возобновлена'
        messages.success(request, f'Задача "{task.title}" {status_text}')
    except Progress.DoesNotExist:
        messages.error(request, 'Задача не найдена')
    
    return redirect('users:cabinet')