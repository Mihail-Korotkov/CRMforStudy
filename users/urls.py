from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('cabinet/', views.UserCabinetView.as_view(), name='cabinet'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('users-list/', views.UserListView.as_view(), name='users-list'),
    path('cabinet/update-profile/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('cabinet/change-password/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('logout/', views.logout, name = 'logout'),
    path('search/', views.UserListView.as_view(), name='search')
    
    
]