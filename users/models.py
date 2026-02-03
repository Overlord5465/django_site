from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# from works.models import Work
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DirectionOfStudy(models.Model):
    name_of_direction = models.CharField(max_length=100, db_index=True,
                                         verbose_name="Название направления")
    direction_code = models.CharField(max_length=100,
                                      verbose_name="Код направления")

    MASTERS_DEGREE = "MD"
    BACHELORS_DEGREE = "BD"
    LEVEL_OF_TRAINING = (
        (BACHELORS_DEGREE, "Бакалавриат"),
        (MASTERS_DEGREE, "Магистратура"),
    )
    level_of_training = models.CharField(max_length=100,
                                  verbose_name="Уровень подготовки", blank=True,
                                  default=BACHELORS_DEGREE,
                                  choices=LEVEL_OF_TRAINING,
                                  )

    class Meta:
        verbose_name = "Направление обучения"
        verbose_name_plural = "Направления обучения"

    def __str__(self):
        return '{0}'.format(self.name_of_direction)


class Group(models.Model):
    group_number = models.CharField(max_length=100, db_index=True,
                                    verbose_name="Номер группы")
    direction_of_study = models.ForeignKey(DirectionOfStudy, max_length=100,
                              verbose_name="Направление обучения",
                              on_delete=models.SET_NULL, null=True,
                              related_name='gr', )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return '{0}'.format(self.group_number)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
                                default=None)
    group = models.ForeignKey(Group, max_length=100,
                              verbose_name="Группа",
                              on_delete=models.SET_NULL, null=True,
                              related_name='st')
    scientific_director = models.ForeignKey('Teacher', on_delete=models.SET_NULL,
                                            verbose_name='Научный руководитель',
                                            related_name='st', null=True,
                                            default=None)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.user.first_name

    # APPLIED_MATHEMATICS_AND_COMPUTER_SCIENCE_B = "01.03.02"
    # FUNDAMENTAL_INFORMATICS_AND_INFORMATION_TECHNOLOGY_B = "02.03.02"
    # MATHEMATICAL_SUPPORT_AND_ADMINISTRATION_OF_INFORMATION_SYSTEMS_B = "02.03.03"
    # APPLIED_COMPUTER_SCIENCE_B = "09.03.03"
    # APPLIED_MATHEMATICS_AND_COMPUTER_SCIENCE_M = "01.04.02"
    # FUNDAMENTAL_INFORMATICS_AND_INFORMATION_TECHNOLOGY_M = "02.04.02"
    # INFORMATION_SYSTEMS_AND_TECHNOLOGIES_M = "09.04.02"
    # CHOICE_OF_DIRECTION_OF_STUDY = (
    #     (APPLIED_MATHEMATICS_AND_COMPUTER_SCIENCE_B,
    #      "Прикладная математика и информатика (Бакалавриат)"),
    #     (FUNDAMENTAL_INFORMATICS_AND_INFORMATION_TECHNOLOGY_B,
    #      "Фундаментальная информатика и информационные технологии (Бакалавриат)"),
    #     (MATHEMATICAL_SUPPORT_AND_ADMINISTRATION_OF_INFORMATION_SYSTEMS_B,
    #      "Математическое обеспечение и администрирование информационных систем (Бакалавриат)"),
    #     (APPLIED_COMPUTER_SCIENCE_B,
    #      "Прикладная информатика (Бакалавриат)"),
    #     (APPLIED_MATHEMATICS_AND_COMPUTER_SCIENCE_M,
    #      "Прикладная математика и информатика (Магистратура)"),
    #     (FUNDAMENTAL_INFORMATICS_AND_INFORMATION_TECHNOLOGY_M,
    #      "Фундаментальная информатика и информационные технологии (Магистратура)"),
    #     (INFORMATION_SYSTEMS_AND_TECHNOLOGIES_M,
    #      "Информационные системы и технологии (Магистратура)"),
    # )
    # direction_of_study = models.CharField(max_length=100, db_index=True,
    #                               verbose_name="Направление обучения",
    #                                       blank=True,
    #                               default=APPLIED_MATHEMATICS_AND_COMPUTER_SCIENCE_B,
    #                               choices=CHOICE_OF_DIRECTION_OF_STUDY,
    #                               )



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
    department = models.CharField(max_length=100,
                                  verbose_name="Кафедра", blank=True,
                                  default=INFORMATION_TECHNOLOGY,
                                  choices=DEPARTMENT_CHOICES,
                                  )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.user.first_name

    # current_amount_3_course_01_03_02 = models.IntegerField(blank=True,
    #                                                        default=0,
    #                                                        verbose_name="Текущее количество 01.03.02",
    #                                               validators=[
    #                                                   MaxValueValidator(10),
    #                                                   MinValueValidator(0)
    #                                               ]
    #                                               )
    # max_amount_3_course_01_03_02 = models.IntegerField(blank=True, default=5,
    #                                                    verbose_name="Максимальное количество 01.03.02",
    #                                           validators=[
    #                                               MaxValueValidator(10),
    #                                               MinValueValidator(0)
    #                                           ]
    #                                           )
    # current_amount_3_course_02_03_02 = models.IntegerField(blank=True,
    #                                                        default=0,
    #                                                        verbose_name="Текущее количество 02.03.02",
    #                                                        validators=[
    #                                                            MaxValueValidator(
    #                                                                10),
    #                                                            MinValueValidator(
    #                                                                0)
    #                                                        ]
    #                                                        )
    # max_amount_3_course_02_03_02 = models.IntegerField(blank=True, default=5,
    #                                                    verbose_name="Максимальное количество 02.03.02",
    #                                                    validators=[
    #                                                        MaxValueValidator(10),
    #                                                        MinValueValidator(0)
    #                                                    ]
    #                                                    )
    # current_amount_3_course_02_03_03 = models.IntegerField(blank=True,
    #                                                        default=0,
    #                                                        verbose_name="Текущее количество 02.03.03",
    #                                                        validators=[
    #                                                            MaxValueValidator(
    #                                                                10),
    #                                                            MinValueValidator(
    #                                                                0)
    #                                                        ]
    #                                                        )
    # max_amount_3_course_02_03_03 = models.IntegerField(blank=True, default=5,
    #                                                    verbose_name="Максимальное количество 02.03.03",
    #                                                    validators=[
    #                                                        MaxValueValidator(10),
    #                                                        MinValueValidator(0)
    #                                                    ]
    #                                                    )
    # current_amount_3_course_09_03_03 = models.IntegerField(blank=True,
    #                                                        default=0,
    #                                                        verbose_name="Текущее количество 09.03.03",
    #                                                        validators=[
    #                                                            MaxValueValidator(
    #                                                                10),
    #                                                            MinValueValidator(
    #                                                                0)
    #                                                        ]
    #                                                        )
    # max_amount_3_course_09_03_03 = models.IntegerField(blank=True, default=5,
    #                                                    verbose_name="Максимальное количество 09.03.03",
    #                                                    validators=[
    #                                                        MaxValueValidator(10),
    #                                                        MinValueValidator(0)
    #                                                    ]
    #                                                    )
    # current_amount_m_01_04_02 = models.IntegerField(blank=True, default=0,
    #                                                 verbose_name="Текущее "
    #                                                              "количество 01.04.02",
    #                                        validators=[
    #                                            MaxValueValidator(10),
    #                                            MinValueValidator(0)
    #                                        ]
    #                                        )
    # max_amount_m_01_04_02 = models.IntegerField(blank=True, default=5,
    #                                             verbose_name="Максимальное "
    #                                                          "количество 01.04.02",
    #                                    validators=[
    #                                        MaxValueValidator(10),
    #                                        MinValueValidator(0)
    #                                    ]
    #                                    )
    # current_amount_m_02_04_02 = models.IntegerField(blank=True, default=0,
    #                                                 verbose_name="Текущее "
    #                                                              "количество "
    #                                                              "02.04.02",
    #                                                 validators=[
    #                                                     MaxValueValidator(10),
    #                                                     MinValueValidator(0)
    #                                                 ]
    #                                                 )
    # max_amount_m_02_04_02 = models.IntegerField(blank=True, default=5,
    #                                             verbose_name="Максимальное "
    #                                                          "количество "
    #                                                          "02.04.02",
    #                                             validators=[
    #                                                 MaxValueValidator(10),
    #                                                 MinValueValidator(0)
    #                                             ]
    #                                             )
    # current_amount_m_09_04_02 = models.IntegerField(blank=True, default=0,
    #                                                 verbose_name="Текущее "
    #                                                              "количество "
    #                                                              "09.04.02",
    #                                                 validators=[
    #                                                     MaxValueValidator(10),
    #                                                     MinValueValidator(0)
    #                                                 ]
    #                                                 )
    # max_amount_m_09_04_02 = models.IntegerField(blank=True, default=5,
    #                                             verbose_name="Максимальное "
    #                                                          "количество "
    #                                                          "09.04.02",
    #                                             validators=[
    #                                                 MaxValueValidator(10),
    #                                                 MinValueValidator(0)
    #                                             ]
    #                                             )




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

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.work.name


class InformationAboutTheNumberOfSeats(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE,
                                verbose_name="Преподаватель", default=0,
                             related_name='teacher')
    direction_of_study = models.ForeignKey('DirectionOfStudy',on_delete=models.CASCADE,
                                           verbose_name="Направление обучения", default=0,
                             related_name='direction')
    current_amount = models.IntegerField(blank=True, default=5,
                                                verbose_name="Текущее количество",
                                       validators=[
                                           MaxValueValidator(10),
                                           MinValueValidator(0)
                                       ]
                                       )
    max_amount = models.IntegerField(blank=True, default=5,
                                                verbose_name="Максимальное количество",
                                       validators=[
                                           MaxValueValidator(10),
                                           MinValueValidator(0)
                                       ]
                                       )

    class Meta:
        verbose_name = "Информация о количестве мест"
        verbose_name_plural = "Информация о количестве мест"
        constraints = [models.UniqueConstraint(fields=['teacher', 'direction_of_study'], name='some_unique_name')]

    def __str__(self):
        return "Информация о количестве мест"
