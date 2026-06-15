from django.contrib.auth.models import AbstractUser
from django.db import models


class RegistrationSettings(models.Model):
    """
    Одна запись в БД: секретный код для регистрации студентов.
    Меняется администраторами кафедры (или суперпользователем) в Django admin.
    """

    code = models.CharField(
        max_length=256,
        verbose_name="Код приглашения",
        help_text="Студенты вводят этот код на странице регистрации. Смените код, чтобы отозвать старые «приглашения».",
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    class Meta:
        verbose_name = "Код регистрации студентов"
        verbose_name_plural = "Код регистрации студентов"

    def __str__(self) -> str:                    
        return "Код регистрации"


class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = "student", "Студент"
        TEACHER = "teacher", "Преподаватель"
        DEPARTMENT_ADMIN = "department_admin", "Администратор кафедры"

    user_type = models.CharField(
        max_length=32,
        choices=UserType.choices,
        default=UserType.STUDENT,
        db_index=True,
        verbose_name="Тип пользователя",
    )

    def __str__(self) -> str:                    
        return self.username
