from django import forms

from users.models import Student
from works.models import Work


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
        fields = ('type_of_work', 'name', 'description', 'author', 'scientific_director', 'file_word',
                  'is_completed')
        labels = {
            'type_of_work': 'Тип работы: ',
            'name': 'Тема: ',
            'description': 'Краткое описание: ',
            'author': 'Автор: ',
            'scientific_director': 'Научный руководитель: ',
            'file_word': 'Текущая версия работы: ',
            'is_completed': 'Работа завершена: ',
        }
