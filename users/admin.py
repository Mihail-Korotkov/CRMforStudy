from django.contrib import admin

# Register your models here.
from users.models import Users
from users.models import Progress
from users.models import Tasks


admin.site.register(Users)


admin.site.register(Progress)


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    # Список полей, которые будут отображаться в таблице (list view)
    list_display = (
        'title', 
        'status', 
        'created_at', 
        'updated_at' ,
        'description'
    )
    
    # Поля, по которым можно фильтровать (справа панель фильтров)
    list_filter = ('status', 'created_at', 'updated_at')
    
    # Поля, по которым можно искать (появляется поле поиска)
    search_fields = ('title', 'description')
    
    # Поля, которые можно редактировать прямо в списке (без перехода внутрь)
    list_editable = ('status',)
    
    # Поля, которые можно сортировать (кликая по заголовку)
    ordering = ('created_at',)  # минус = по убыванию (сначала новые)
    
    # Какие поля показывать на странице редактирования (detail view)
    fields = ('title', 'description', 'status', 'created_at', 'updated_at')
    
    # Какие поля только для чтения (нельзя редактировать)
    readonly_fields = ('created_at', 'updated_at')