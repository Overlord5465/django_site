import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from users.models import Teacher, Student


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "ФИО",
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    # username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    #date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(
    # range(this_year-100, this_year-5))))

    class Meta:
        model = get_user_model()
        fields = ['username',
                  'email',
                  'first_name']
        labels = {
            'username': 'Логин',
            'email': 'Адрес электронной почты',
            'first_name': 'ФИО',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email')
        labels = {
            'first_name': 'ФИО',
            'email': 'Адрес электронной почты',
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('course', 'group')

        labels = {
            'course': 'Курс',
            'group': 'Номер группы',
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('department',
                  'current_amount_3_course',
                  'max_amount_3_course',
                  'current_amount_4_course',
                  'max_amount_4_course',
                  'current_amount_m',
                  'max_amount_m',
                  )
        labels = {'department': 'Кафедра',
                  'current_amount_3_course': 'Текущее количество 3-его курса',
                  'max_amount_3_course': 'Максимальное количество 3-его курса',
                  'current_amount_4_course': 'Текущее количество 4-ого курса',
                  'max_amount_4_course': 'Максимальное количество 4-ого курса',
                  'current_amount_m': 'Текущее количество магистратуры',
                  'max_amount_m': 'Максимальное количество магистратуры'
        }
