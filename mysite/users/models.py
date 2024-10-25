from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from works.models import Work
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
                                default=None)
    course = models.IntegerField(blank=True, default=3, verbose_name="Курс")
    group = models.CharField(max_length=100, db_index=True,
                             verbose_name="Группа", blank=True)


@receiver(post_save, sender=User)
def create_user_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_student(sender, instance, **kwargs):
    is_student = Student.objects.filter(user=instance.pk).exists()
    if is_student:
        instance.student.save()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
                                default=None)
    INFORMATION_TECHNOLOGY = "IT"
    COMPUTATIONAL_TECHNOLOGIES = "CT"
    MATHEMATICAL_MODELING = "MM"
    DATA_ANALYSIS_AND_ARTIFICIAL_INTELLIGENCE = "DAAAI"
    APPLIED_MATHEMATICS = "AM"
    DEPARTMENT_CHOICES = (
        (INFORMATION_TECHNOLOGY, "Кафедра информационных технологий"),
        (COMPUTATIONAL_TECHNOLOGIES, "Кафедра вычислительных технологий"),
        (MATHEMATICAL_MODELING, "Кафедра математического моделирования"),
        (DATA_ANALYSIS_AND_ARTIFICIAL_INTELLIGENCE, "Кафедра анализа данных и искусственного интеллекта"),
        (APPLIED_MATHEMATICS, "Кафедра прикладной математики"),
    )
    department = models.CharField(max_length=100, db_index=True,
                                  verbose_name="Кафедра", blank=True,
                                  default=INFORMATION_TECHNOLOGY,
                                  choices=DEPARTMENT_CHOICES,
                                  )
    current_amount_3_course = models.IntegerField(blank=True, default=0,
                                                  validators=[
                                                      MaxValueValidator(5),
                                                      MinValueValidator(0)
                                                  ]
                                                  )
    max_amount_3_course = models.IntegerField(blank=True, default=5,
                                              validators=[
                                                  MaxValueValidator(5),
                                                  MinValueValidator(0)
                                              ]
                                              )
    current_amount_4_course = models.IntegerField(blank=True, default=0,
                                                  validators=[
                                                      MaxValueValidator(5),
                                                      MinValueValidator(0)
                                                  ]
                                                  )
    max_amount_4_course = models.IntegerField(blank=True, default=5,
                                              validators=[
                                                  MaxValueValidator(5),
                                                  MinValueValidator(0)
                                              ]
                                              )
    current_amount_m = models.IntegerField(blank=True, default=0,
                                           validators=[
                                               MaxValueValidator(5),
                                               MinValueValidator(0)
                                           ]
                                           )
    max_amount_m = models.IntegerField(blank=True, default=5,
                                       validators=[
                                           MaxValueValidator(5),
                                           MinValueValidator(0)
                                       ]
                                       )


# @receiver(post_save, sender=User)
# def create_user_teacher(sender, instance, created, **kwargs):
#     if created:
#         Teacher.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_teacher(sender, instance, **kwargs):
#     instance.teacher.save()


class Message(models.Model):
    work = models.ForeignKey('works.Work', on_delete=models.SET_NULL,
                             related_name='messages1', null=True, default=None)
    text = models.CharField(max_length=100, db_index=True,
                            verbose_name="Категория")
    sender = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='messages2', null=True,
                               default=None)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                  related_name='messages3', null=True,
                                  default=None)
