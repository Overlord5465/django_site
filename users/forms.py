import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from users.models import Teacher, Student, Group


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин: ",
                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль: ",
                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля:", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail:',
            'first_name': "ФИО:",
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
    old_password = forms.CharField(label="Старый пароль: ", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль: ", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля: ", widget=forms.PasswordInput(attrs={'class':
                                                                                                         'form-input'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email')
        labels = {
            'first_name': 'ФИО',
            'email': 'Адрес электронной почты',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('group',)

        labels = {
            'group': 'Номер группы: ',
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('department',
                  # 'current_amount_3_course_01_03_02',
                  # 'max_amount_3_course_01_03_02',
                  # 'current_amount_3_course_02_03_02',
                  # 'max_amount_3_course_02_03_02',
                  # 'current_amount_3_course_02_03_03',
                  # 'max_amount_3_course_02_03_03',
                  # 'current_amount_3_course_09_03_03',
                  # 'max_amount_3_course_09_03_03',
                  # 'current_amount_m_01_04_02',
                  # 'max_amount_m_01_04_02',
                  # 'current_amount_m_02_04_02',
                  # 'max_amount_m_02_04_02',
                  # 'current_amount_m_09_04_02',
                  # 'max_amount_m_09_04_02'
                  )
        labels = {'department': 'Кафедра: ',
                  # 'current_amount_3_course_01_03_02':
                  #     'Текущее количество бакалавриат (01.03.02)',
                  # 'max_amount_3_course_01_03_02':
                  #     'Максимальное количество бакалавриат (01.03.02)',
                  # 'current_amount_3_course_02_03_02':
                  #     'Текущее количество бакалавриат (02.03.02)',
                  # 'max_amount_3_course_02_03_02':
                  #     'Максимальное количество бакалавриат (02.03.02)',
                  # 'current_amount_3_course_02_03_03':
                  #     'Текущее количество бакалавриат (02.03.03)',
                  # 'max_amount_3_course_02_03_03':
                  #     'Максимальное количество бакалавриат (02.03.03)',
                  # 'current_amount_3_course_09_03_03':
                  #     'Текущее количество бакалавриат (09.03.03)',
                  # 'max_amount_3_course_09_03_03':
                  #     'Максимальное количество бакалавриат (09.03.03)',
                  # 'current_amount_m_01_04_02':
                  #     'Текущее количество магистратуры (01.04.02)',
                  # 'max_amount_m_01_04_02':
                  #     'Максимальное количество магистратуры (01.04.02)',
                  # 'current_amount_m_02_04_02':
                  #     'Текущее количество магистратуры (02.04.02)',
                  # 'max_amount_m_02_04_02':
                  #     'Максимальное количество магистратуры (02.04.02)',
                  # 'current_amount_m_09_04_02':
                  #     'Текущее количество магистратуры (09.04.02)',
                  # 'max_amount_m_09_04_02':
                  #     'Максимальное количество магистратуры (09.04.02)'
        }
