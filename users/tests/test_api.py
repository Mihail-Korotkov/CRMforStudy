from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from users.models import Users


class TestCRMAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Users.objects.create_superuser(
            username='admin',
            email='admin@mail.com',
            password='admin123'
        )
        self.user = Users.objects.create_user(
            username='testuser',
            email='test@mail.com',
            password='testpass123'
        )
        self.url = '/user/api/users/'

    def test_api_requires_admin(self):
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    