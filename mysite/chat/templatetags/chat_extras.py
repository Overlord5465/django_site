from django import template

from chat.utils import chat_separator_date_label

register = template.Library()


@register.filter
def chat_day_ru(value):
    """Дата для разделителя: день + месяц на русском (например «17 апреля»)."""
    if not value:
        return ""
    return chat_separator_date_label(value)
