import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from django.core.exceptions import ValidationError

from users.models import RegistrationSettings
from profiles.fio_utils import apply_full_fio_to_user, format_user_fio
from profiles.models import DirectionOfStudy, Student, Group


def _initial_fio_in_first_name_field(form: forms.ModelForm) -> None:
    """В БД фамилия в last_name, имя+отчество в first_name; в поле «ФИО» показываем полную строку."""
    if not getattr(form.instance, "pk", None):
        return
    if "first_name" not in form.fields:
        return
    form.initial["first_name"] = format_user_fio(form.instance)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин: ",
                    widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    password = forms.CharField(label="Пароль: ",
                    widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    registration_code = forms.CharField(
        label="Код приглашения:",
        max_length=256,
        strip=True,
        widget=forms.TextInput(
            attrs={"class": "form-control form-input", "autocomplete": "off", "placeholder": "Выдаётся администратором кафедры"}
        ),
    )
    username = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    email = forms.EmailField(
        label="Электронная почта:",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control form-input'}),
    )
    password1 = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))
    password2 = forms.CharField(label="Повтор пароля:", widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))
    group = forms.ModelChoiceField(
        label="Группа:",
        queryset=Group.objects.select_related("direction_of_study").order_by("group_number"),
        empty_label="Выберите группу",
        widget=forms.Select(attrs={"class": "form-select form-input"}),
    )
    field_order = [
        "registration_code",
        "username",
        "first_name",
        "email",
        "group",
        "password1",
        "password2",
    ]
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'password1', 'password2']
        labels = {
            'first_name': "ФИО:",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _initial_fio_in_first_name_field(self)

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        settings_obj = RegistrationSettings.objects.order_by("-updated_at").first()
        expected = (settings_obj.code if settings_obj else "") or ""
        expected = expected.strip()
        if not expected:
            raise ValidationError(
                "Регистрация временно недоступна: администратор кафедры не задал код приглашения в административной панели."
            )
        entered = (cleaned_data.get("registration_code") or "").strip()
        if entered != expected:
            self.add_error(
                "registration_code",
                "Неверный код приглашения. Обратитесь к администратору кафедры.",
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        apply_full_fio_to_user(user, self.cleaned_data.get("first_name", ""))
        if commit:
            user.save()
        return user


class ProfileUserForm(forms.ModelForm):
                                                                                                                     
                                                                                                                   
                                                                            
                                          

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
            'username': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _initial_fio_in_first_name_field(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        apply_full_fio_to_user(user, self.cleaned_data.get("first_name", ""))
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль: ", widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))
    new_password1 = forms.CharField(label="Новый пароль: ", widget=forms.PasswordInput(attrs={'class': 'form-control form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля: ", widget=forms.PasswordInput(attrs={'class':
                                                                                                         'form-control form-input'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email')
        labels = {
            'first_name': 'ФИО',
            'email': 'Адрес электронной почты',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _initial_fio_in_first_name_field(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        apply_full_fio_to_user(user, self.cleaned_data.get("first_name", ""))
        if commit:
            user.save()
        return user


class DepartmentAdminProfileForm(forms.ModelForm):
    """Профиль администратора кафедры (без записей Student/Teacher). Кафедра задаётся в админке."""

    class Meta:
        model = get_user_model()
        fields = ("first_name", "email")
        labels = {
            "first_name": "ФИО",
            "email": "Адрес электронной почты",
        }
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control form-input"}),
            "first_name": forms.TextInput(attrs={"class": "form-control form-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _initial_fio_in_first_name_field(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        apply_full_fio_to_user(user, self.cleaned_data.get("first_name", ""))
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = tuple()

        labels = {
            'group': 'Группа: ',
        }
        widgets = {
            "group": forms.Select(attrs={"class": "form-select form-input"}),
        }

                                                                                    
