

import stat

from django.test import TestCase

from users.utils import count_leaders, get_leader_name, get_max_progress,get_users_with_stats

from users.models import Users, Tasks, Progress




class UtilsTests(TestCase):

    def setUp(self):
        
        self.user1 = Users.objects.create(username='user1', email='user1@example.com', password='password',role = "backend")

        self.user2 = Users.objects.create(username='user2', email='user2@example.com', password='password',role = "frontend")

        self.task1 = Tasks.objects.create(title = 'task1', description = 'task1 description', status = True )
        self.task2 = Tasks.objects.create(title = 'task2', description = 'task2 description' ,status = True )
        self.task3 = Tasks.objects.create(title = 'task3', description = 'task3 description' ,status = False )


        Progress.objects.create(user = self.user1, task = self.task1)
        Progress.objects.create(user = self.user1, task = self.task2)
        Progress.objects.create(user = self.user2, task = self.task1)
        Progress.objects.create(user = self.user2, task = self.task3)




    def test_count_leaders(self):
        ch = count_leaders()
        self.assertEqual(ch, 1)


    def test_get_leader_name(self):
        name = get_leader_name()
        self.assertEqual(name,"user1")



    def test_get_users_with_stats(self):
        users = get_users_with_stats()

        user1 = users.get(id = self.user1.id)
        user2 = users.get(id = self.user2.id)

        self.assertEqual(user1.total_tasks,2)
        self.assertEqual(user2.total_tasks,2)

    def test_get_max_progress(self):
        max_progress = get_max_progress()
        self.assertEqual(max_progress,100)
        





        