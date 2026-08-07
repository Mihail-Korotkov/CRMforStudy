from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import Users




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields = ('username', 'password')





class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    
    
    


