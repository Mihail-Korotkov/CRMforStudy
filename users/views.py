from datetime import timedelta

from django.contrib import auth
from django.shortcuts import get_list_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Case, Count, ExpressionWrapper, FloatField, IntegerField, Value, When
from django.db.models.functions import Cast

from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from users.utils import count_leaders, get_leader_name, get_max_progress, get_users_with_stats



from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateProfileForm


from users.models import Progress, Tasks, Users
from users.utils import get_activity_for_user, new_users_last_week, q_search



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
        context['get_activity_for_week'] = get_activity_for_user(user)
    
        total = user_progress.count()
        if total > 0:
            context['user_progress'] = int((completed_tasks.count() / total) * 100)
        else:
            context['user_progress'] = 0
            
        context['activity_percentage'] = 94  
        
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
    success_url = reverse_lazy("main:index")
    failure_url = "users:registration"
    success_message = "Вы успешно зарегистрировались"
    failure_message = "Неверные данные"
    
    def form_valid(self, form):
        
        # Сохраняем пользователя
        response = super().form_valid(form)

        
        # Автоматически входим
        login(self.request, self.object)
        messages.success(self.request, self.success_message)
        return response
    
    def form_invalid(self, form):
        # Если форма невалидна, показываем ошибки
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


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
    paginate_by = 3

    

    def get_queryset(self):
        # role_filter = self.request.GET.get("role")
        # order_by = self.request.GET.get("order_by")
        query = self.request.GET.get('q')
        filter_type = self.request.GET.get('filter', 'all')  
        sort_by = self.request.GET.get('sort', 'id')

         # 🔍 ОТЛАДКА - проверяем параметры
        print(f"🔍 Фильтр: {filter_type}, Сортировка: {sort_by}, Поиск: {query}")
        

        users = get_users_with_stats()
        if filter_type == "leaders":
            max_progress = get_max_progress()
            users = users.filter(progress_percent=max_progress, progress_percent__gt=0)
        if filter_type == "new":
            users = users.filter(date_joined__gte=timezone.now() - timedelta(days=7))
        

        
 
        if query:
            users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )
            print(f"🔍 Применен поиск: {query}")

        if sort_by == "progress-desc":
            users = users.order_by('-progress_percent','id')
            print(f"🔍 Сортировка: по прогрессу ↓")
        elif sort_by == "progress-asc":
            users = users.order_by('progress_percent','id')
            print(f"🔍 Сортировка: по прогрессу ↑")
        elif sort_by == "tasks":
            users = users.order_by('-completed_tasks','id')
            print(f"🔍 Сортировка: по задачам ↓")
        else:
            users = users.order_by('id')
            print(f"🔍 Сортировка: по умолчанию (ID)")
        print(f"🔍 Найдено пользователей: {users.count()}")
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Users.objects.count()
        context['new_in_last_week'] = new_users_last_week()
        context['count_leaders'] = count_leaders()
        context['leader_name'] = get_leader_name()
        context['max_progress'] = get_max_progress()

        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['current_sort'] = self.request.GET.get('sort', 'id')
        context['search_query'] = self.request.GET.get('q', '')
        return context


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