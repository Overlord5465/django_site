def apply_full_fio_to_user(user, full_name: str) -> None:
    """
    Заполняет user.last_name и user.first_name из одной строки «Фамилия Имя Отчество».

    В формах профиля и регистрации поле подписано «ФИО», но технически привязано к first_name;
    без этого last_name остаётся старым, и отображение даёт дубль фамилии.
    """
    full_name = (full_name or "").strip()
    if not full_name:
        user.last_name = ""
        user.first_name = ""
        return
    parts = full_name.split()
    if len(parts) >= 2:
        user.last_name = parts[0]
        user.first_name = " ".join(parts[1:])
    else:
        user.last_name = full_name
        user.first_name = ""


def format_user_fio(user) -> str:
    """Строка для интерфейса: «Фамилия Имя Отчество» из полей User."""
    if not user:
        return ""
    last = (getattr(user, "last_name", None) or "").strip()
    first = (getattr(user, "first_name", None) or "").strip()
    if last and first:
        return f"{last} {first}".strip()
    if last:
        return last
    if first:
        return first
    full = (user.get_full_name() or "").strip()
    if full:
        return full
    return (getattr(user, "username", None) or "").strip() or ""
