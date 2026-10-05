# from rest_framework.test import APIClient, APITestCase
# from rest_framework import status

# from users.models import Users

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Users


# class TestCRMAPI(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.admin = Users.objects.create_superuser(
#             username='admin',
#             email='admin@mail.com',
#             password='admin123'
#         )
#         self.user = Users.objects.create_user(
#             username='testuser',
#             email='test@mail.com',
#             password='testpass123'
#         )
#         self.url = '/user/api/users/'

#     def test_api_requires_admin(self):
        
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



# -----------------------------------------------------------------pytest------------------------------------------------        

class TestUserAPI:
    """Тесты API пользователей"""
    
    url = '/user/api/users/'
    
    def test_api_requires_auth(self, api_client):
        """Тест: API требует авторизации"""
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_api_requires_admin(self, api_client, regular_user):
        """Тест: API требует прав админа"""
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_api_admin_access(self, api_client, admin_user):
        """Тест: админ имеет доступ"""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_api_returns_users(self, api_client, admin_user, regular_user):
        """Тест: API возвращает список пользователей"""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2




