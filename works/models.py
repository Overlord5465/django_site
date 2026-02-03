from django.contrib.auth import get_user_model
from django.db import models
from django.http import HttpResponseRedirect

from users.models import Student, Teacher


class Work(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Название")
    description = models.CharField(max_length=100,
                                   verbose_name="Описание")
    type_of_work = models.CharField(max_length=100,
                                    verbose_name="Тип работы")
    year = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", blank=True)
    author = models.ForeignKey(Student, max_length=100,
                               verbose_name="Автор",
                               on_delete=models.SET_NULL, null=True,
                               related_name='st',)
    scientific_director = models.ForeignKey(Teacher, max_length=100, related_name='sd',
                                            verbose_name="Научный руководитель",
                                            on_delete=models.SET_NULL, null=True)
    file_word = models.FileField(upload_to='uploads_model')

    is_completed = models.BooleanField(verbose_name="Статус")


def add_student(request):
    if request.method == "POST":
        work = Work()
        work.author = request.POST.get("student")
        work.scientific_director = request.POST.get("teacher")
        work.save()
    return HttpResponseRedirect("/")
