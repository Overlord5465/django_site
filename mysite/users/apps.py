from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # Путь пакета Python после переименования папки приложения.
    name = "users"
    # Исторический label приложения: имена таблиц в БД и AUTH_USER_MODEL не меняются.
    label = "accounts"
