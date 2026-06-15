from django import forms

from profiles.fio_utils import format_user_fio
from profiles.models import Teacher
from works.models import StudentTopicProposal, Topic, TopicApplication


def _teacher_choice_label(teacher: Teacher) -> str:
    if teacher.user_id:
        return format_user_fio(teacher.user)
    return str(teacher.pk)


_TOPIC_FIELD_STYLE = "width:100%;box-sizing:border-box;"


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("title", "description", "work_kind")
        labels = {
            "title": "Название темы",
            "description": "Описание",
            "work_kind": "Тип работы",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control w-100", "style": _TOPIC_FIELD_STYLE}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control w-100",
                    "style": f"{_TOPIC_FIELD_STYLE}resize:vertical;",
                    "rows": 5,
                }
            ),
            "work_kind": forms.Select(attrs={"class": "form-select w-100"}),
        }


class DepartmentTopicForm(TopicForm):
    """Админ кафедры указывает преподавателя-владельца темы."""

    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.none(),
        label="Преподаватель (автор темы в банке)",
        widget=forms.Select(attrs={"class": "form-select w-100"}),
    )

    def __init__(self, *args, teacher_qs=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher_qs is not None:
            self.fields["teacher"].queryset = teacher_qs


class ProposeTopicForm(forms.Form):
    _text_widget_attrs = {
        "class": "form-control w-100",
        "style": "width:100%;box-sizing:border-box;resize:vertical;min-height:2.75rem;",
    }

    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.select_related("user").order_by(
            "department", "user__last_name", "user__first_name"
        ),
        label="Преподаватель",
        empty_label="Выберите преподавателя",
        widget=forms.Select(attrs={"class": "form-select w-100"}),
    )
    title = forms.CharField(
        max_length=200,
        label="Тема (название)",
        widget=forms.Textarea(attrs={**_text_widget_attrs, "rows": 2}),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={**_text_widget_attrs, "rows": 5}),
        label="Описание работы",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teacher"].label_from_instance = _teacher_choice_label


class StudentTopicProposalDecisionForm(forms.ModelForm):
    class Meta:
        model = StudentTopicProposal
        fields = ("status", "decision_comment")
        labels = {"status": "Решение", "decision_comment": "Комментарий"}
        widgets = {
            "status": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "decision_comment": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 4}),
        }


class TopicApplicationDecisionForm(forms.ModelForm):
    class Meta:
        model = TopicApplication
        fields = ("status", "decision_comment")
        labels = {"status": "Решение", "decision_comment": "Комментарий"}
        widgets = {
            "status": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "decision_comment": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 4}),
        }
