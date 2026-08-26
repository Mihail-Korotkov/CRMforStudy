from django.urls import path
from main import views
from django.views.decorators.cache import cache_page


app_name = 'main'


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('about/',cache_page(60*5)(views.AboutView.as_view()), name='about'),
    
]