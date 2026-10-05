# users/tests/conftest.py
import pytest
from users.models import Users, Tasks, Progress
from rest_framework.test import APIClient



@pytest.fixture
def user1(db):
    """Создаёт первого пользователя"""
    return Users.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='password',
        role='backend'
    )


@pytest.fixture
def user2(db):
    """Создаёт второго пользователя"""
    return Users.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='password',
        role='frontend'
    )


@pytest.fixture
def task1(db):
    """Выполненная задача"""
    return Tasks.objects.create(
        title='task1',
        description='task1 description',
        status=True
    )


@pytest.fixture
def task2(db):
    """Выполненная задача"""
    return Tasks.objects.create(
        title='task2',
        description='task2 description',
        status=True
    )


@pytest.fixture
def task3(db):
    """Невыполненная задача"""
    return Tasks.objects.create(
        title='task3',
        description='task3 description',
        status=False
    )


@pytest.fixture
def progress_data(db, user1, user2, task1, task2, task3):
    """
    Создаёт все связи Progress:
    - user1: task1 (выполнена) + task2 (выполнена) → 100%
    - user2: task1 (выполнена) + task3 (не выполнена) → 50%
    """
    Progress.objects.create(user=user1, task=task1)
    Progress.objects.create(user=user1, task=task2)
    Progress.objects.create(user=user2, task=task1)
    Progress.objects.create(user=user2, task=task3)
    
    return {
        'user1': user1,
        'user2': user2,
        'task1': task1,
        'task2': task2,
        'task3': task3,
    }

@pytest.fixture
def setup_data(db):
    """Создаёт тестовые данные"""
    user1 = Users.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='password',
        role='backend'
    )
    user2 = Users.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='password',
        role='frontend'
    )
    
    task1 = Tasks.objects.create(
        title='task1', description='...', status=True
    )
    task2 = Tasks.objects.create(
        title='task2', description='...', status=True
    )
    task3 = Tasks.objects.create(
        title='task3', description='...', status=False
    )
    
    Progress.objects.create(user=user1, task=task1)
    Progress.objects.create(user=user1, task=task2)
    Progress.objects.create(user=user2, task=task1)
    Progress.objects.create(user=user2, task=task3)
    
    return {
        'user1': user1,
        'user2': user2,
        'task1': task1,
        'task2': task2,
        'task3': task3,
    }
# -------------------------фикстуры для теста апи--------------------------   
@pytest.fixture
def api_client():
    """API клиент для запросов"""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """Суперпользователь (админ)"""
    return Users.objects.create_superuser(
        username='admin',
        email='admin@mail.com',
        password='admin123'
    )


@pytest.fixture
def regular_user(db):
    """Обычный пользователь"""
    return Users.objects.create_user(
        username='testuser',
        email='test@mail.com',
        password='testpass123'
    )


