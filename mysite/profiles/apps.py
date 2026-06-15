from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Путь пакета Python после переименования папки приложения.
    name = "profiles"
    # Исторический label приложения: имена таблиц в БД и история миграций сохраняются.
    label = "users"
