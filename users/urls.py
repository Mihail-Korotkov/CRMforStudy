from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('cabinet/', views.UserCabinetView.as_view(), name='cabinet'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('users-list/', views.UserListView.as_view(), name='users-list')
]