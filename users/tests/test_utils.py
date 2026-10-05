

# import stat

# from django.test import TestCase
import pytest

from users.utils import count_leaders, get_leader_name, get_max_progress,get_users_with_stats, plus

from users.models import Users, Tasks, Progress




# class UtilsTests(TestCase):

#     def setUp(self):
        
#         self.user1 = Users.objects.create(username='user1', email='user1@example.com', password='password',role = "backend")

#         self.user2 = Users.objects.create(username='user2', email='user2@example.com', password='password',role = "frontend")

#         self.task1 = Tasks.objects.create(title = 'task1', description = 'task1 description', status = True )
#         self.task2 = Tasks.objects.create(title = 'task2', description = 'task2 description' ,status = True )
#         self.task3 = Tasks.objects.create(title = 'task3', description = 'task3 description' ,status = False )


#         Progress.objects.create(user = self.user1, task = self.task1)
#         Progress.objects.create(user = self.user1, task = self.task2)
#         Progress.objects.create(user = self.user2, task = self.task1)
#         Progress.objects.create(user = self.user2, task = self.task3)




#     def test_count_leaders(self):
#         ch = count_leaders()
#         self.assertEqual(ch, 1)


#     def test_get_leader_name(self):
#         name = get_leader_name()
#         self.assertEqual(name,"user1")



#     def test_get_users_with_stats(self):
#         users = get_users_with_stats()

#         user1 = users.get(id = self.user1.id)
#         user2 = users.get(id = self.user2.id)

#         self.assertEqual(user1.total_tasks,2)
#         self.assertEqual(user2.total_tasks,2)

#     def test_get_max_progress(self):
#         max_progress = get_max_progress()
#         self.assertEqual(max_progress,100)
# -----------------------------------------------------------------pytest------------------------------------------------        


def test_count_leaders(setup_data):
    """Тест: подсчёт лидеров (должен быть 1)"""
    # user1: 100%, user2: 50% → 1 лидер
    result = count_leaders()
    assert result == 1


def test_get_leader_name(setup_data):
    """Тест: имя лидера"""
    result = get_leader_name()
    assert result == 'user1'


def test_get_users_with_stats(setup_data):
    """Тест: аннотации пользователей"""
    users = get_users_with_stats()
    
    user1 = users.get(id=setup_data['user1'].id)
    user2 = users.get(id=setup_data['user2'].id)
    
    # user1: 2 задачи, 2 выполнены → 100%
    assert user1.total_tasks == 2
    assert user1.completed_tasks == 2
    assert user1.progress_percent == 100
    
    # user2: 2 задачи, 1 выполнена → 50%
    assert user2.total_tasks == 2
    assert user2.completed_tasks == 1
    assert user2.progress_percent == 50


def test_get_max_progress(setup_data):
    """Тест: максимальный прогресс"""
    result = get_max_progress()
    assert result == 100


def test_get_users_with_stats_no_users(db):
    """Тест: нет пользователей"""
    users = get_users_with_stats()
    assert users.count() == 0


def test_get_max_progress_no_users(db):
    """Тест: нет пользователей → 0"""
    result = get_max_progress()
    assert result == 0







        