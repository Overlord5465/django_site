from django import forms

from profiles.models import Student
from works.models import (
    IndividualPlan,
    PlanStage,
    Work,
)

COURSE_ANNOUNCEMENT_CHOICES = [(i, f"{i} курс") for i in range(1, 9)]


class SearchForm(forms.Form):
    query = forms.CharField()


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('scientific_director',)
        labels = {
            'scientific_director': 'Научный руководитель',
        }


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ("type_of_work", "name", "description", "author", "scientific_director", "status")
        labels = {
            "type_of_work": "Тип работы: ",
            "name": "Тема: ",
            "description": "Краткое описание: ",
            "author": "Автор: ",
            "scientific_director": "Научный руководитель: ",
            "status": "Статус: ",
        }


class StudentWorkForm(forms.ModelForm):
    """Редактирование работы студентом (без смены автора/руководителя)."""

    class Meta:
        model = Work
        fields = ("type_of_work", "description")
        labels = {
            "type_of_work": "Тип работы: ",
            "description": "Описание: ",
        }


class TeacherWorkTopicForm(forms.ModelForm):
    """Ручная правка темы/описания руководителем."""

    class Meta:
        model = Work
        fields = ("name", "description")
        labels = {"name": "Тема: ", "description": "Краткое описание: "}


class AssignTopicForm(forms.ModelForm):
    """
    Department admin assigns topic by editing Work fields.
    Restricts supervisor choices to admin's department.
    """

    def __init__(self, *args, request_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        dept = getattr(getattr(request_user, "teacher", None), "department", "") if request_user else ""
        if dept:
            self.fields["scientific_director"].queryset = (
                self.fields["scientific_director"].queryset.filter(department=dept)
            )

    class Meta:
        model = Work
        fields = ("type_of_work", "name", "description", "scientific_director")
        labels = {
            "type_of_work": "Тип работы: ",
            "name": "Тема: ",
            "description": "Краткое описание: ",
            "scientific_director": "Научный руководитель: ",
        }


class WorkDocxUploadForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ("docx_file",)
        labels = {"docx_file": "Файл"}


class DepartmentAnnouncementForm(forms.Form):
    course = forms.TypedChoiceField(
        label="Курс обучения (поле «Курс» у учебной группы студента)",
        choices=COURSE_ANNOUNCEMENT_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    body = forms.CharField(
        label="Содержание",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 8}),
    )


class PlanStageForm(forms.ModelForm):
    class Meta:
        model = PlanStage
        fields = ("title", "due_date", "order", "parent")
        labels = {
            "title": "Этап",
            "due_date": "Срок",
            "order": "Порядок",
            "parent": "Вложить в пункт (необязательно)",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "due_date": forms.DateInput(attrs={"class": "form-control form-control-sm", "type": "date"}),
            "order": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 0}),
            "parent": forms.Select(attrs={"class": "form-select form-input"}),
        }

    def __init__(self, *args, plan=None, **kwargs):
        super().__init__(*args, **kwargs)
        if plan is not None:
            qs = plan.stages.all()
            if getattr(self.instance, "pk", None):
                qs = qs.exclude(pk=self.instance.pk)
            self.fields["parent"].queryset = qs
        else:
            self.fields["parent"].queryset = PlanStage.objects.none()
        self.fields["parent"].required = False
        self.fields["parent"].empty_label = "— корневой пункт —"