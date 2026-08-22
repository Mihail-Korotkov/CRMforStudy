from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from users.models import Users
from django.forms import CharField, ImageField




class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    class Meta:
        model = Users
        fields = ('email', 'password')





class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=100,
        help_text='Обязательное поле. Не более 150 символов.'
    )
    email = forms.EmailField(
        label='Email',
        help_text='Введите действующий email'
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Пароль должен содержать не менее 8 символов'
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Введите тот же пароль для подтверждения'
    )

    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        username = cleaned_data.get('username')
        
        # Свои сообщения об ошибках
        if password1 and username:
            if password1.lower() in username.lower() or username.lower() in password1.lower():
                raise forms.ValidationError(
                    'Пароль слишком похож на имя пользователя'
                )
        
        return cleaned_data


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

