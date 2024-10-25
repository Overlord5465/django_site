from django.contrib.auth import get_user_model
from django.db import models


class Work(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Название")
    description = models.CharField(max_length=100, db_index=True,
                                   verbose_name="Описание")
    type_of_work = models.CharField(max_length=100, db_index=True,
                                    verbose_name="Тип работы")
    year = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    author = models.ForeignKey(get_user_model(), max_length=100, db_index=True,
                               verbose_name="Автор",
                               on_delete=models.SET_NULL, null=True,
                               related_name='st',)
    scientific_director = models.ForeignKey(get_user_model(), max_length=100,
                                            db_index=True, related_name='sd',
                                            verbose_name="Научный руководитель",
                                            on_delete=models.SET_NULL, null=True)
    file_word = models.FileField(upload_to='uploads_model')

    is_completed = models.BooleanField(verbose_name="Статус")
