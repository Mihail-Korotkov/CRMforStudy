from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from users.models import Users
from django.forms import CharField, ImageField




class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    class Meta:
        model = Users
        fields = ('email', 'password')





class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = (
            'image',
            'username',
            'email',
            'role',
            'github_url',
            'linkedin_url',
            'telegram_url',
        )
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'telegram_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Аватарка',
            'username': 'Имя пользователя',
            'email': 'Email',
            'role': 'Роль (должность)',
            'github_url': 'Ссылка на GitHub',
            'linkedin_url': 'Ссылка на LinkedIn',
            'telegram_url': 'Ссылка на Telegram',
        }

    # Очистка полей (опционально, можно добавить валидацию)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Проверка, что email не занят другим пользователем
        if Users.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется другим пользователем.')
        return email

