"""Утилиты чата (форматирование дат независимо от LANGUAGE_CODE)."""

from __future__ import annotations

from django.utils import timezone

                                           
_RU_MONTHS_GENITIVE = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)


def chat_separator_date_label(dt) -> str:
    """Строка для разделителя дня: «17 апреля» (месяц на русском)."""
    local = timezone.localtime(dt)
    return f"{local.day} {_RU_MONTHS_GENITIVE[local.month - 1]}"
