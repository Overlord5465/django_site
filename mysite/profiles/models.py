from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

                               
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.course_utils import CourseBucket


class Department(models.Model):
    """Справочник кафедр (подразделений)."""

    code = models.CharField(max_length=32, unique=True, db_index=True, verbose_name="Код")
    name = models.CharField(max_length=200, unique=True, db_index=True, verbose_name="Название")

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедры"
        ordering = ("name",)

    def __str__(self):
        return self.name


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
    course = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Курс",
        help_text="Курс для группы. Бакалавриат: 3 или 4; магистратура: 1 или 2.",
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        db_index=True,
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return '{0}'.format(self.group_number)


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
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


@receiver(post_save, sender=get_user_model())
def create_user_student(sender, instance, created, **kwargs):
    if not created:
        return

    user_type = getattr(instance, "user_type", None)
    if user_type == "student":
        Student.objects.get_or_create(user=instance)
    elif user_type == "teacher":
        Teacher.objects.get_or_create(user=instance)
    elif user_type == "department_admin":
        Teacher.objects.get_or_create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_student(sender, instance, **kwargs):

    user_type = getattr(instance, "user_type", None)
    if user_type == "student":
        Student.objects.get_or_create(user=instance)
    elif user_type == "teacher":
        Teacher.objects.get_or_create(user=instance)
    elif user_type == "department_admin":
        Teacher.objects.get_or_create(user=instance)


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachers",
        verbose_name="Кафедра",
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.user.first_name



class TeacherCourseSeat(models.Model):
    """Лимиты закрепления студентов по курсу (бакалавриат 3/4, магистратура 1/2)."""

    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, related_name="course_seats")
    bucket = models.CharField(max_length=2, choices=CourseBucket.CHOICES, db_index=True)
    current_amount = models.IntegerField(
        default=0,
        verbose_name="Занято",
        validators=[MaxValueValidator(1000), MinValueValidator(0)],
    )
    max_amount = models.IntegerField(
        default=5,
        verbose_name="Лимит",
        validators=[MaxValueValidator(1000), MinValueValidator(0)],
    )

    class Meta:
        verbose_name = "Лимит по курсу"
        verbose_name_plural = "Лимиты по курсам"
        constraints = [
            models.UniqueConstraint(fields=["teacher", "bucket"], name="uniq_teacher_course_bucket"),
        ]

    def __str__(self) -> str:                    
        return f"{self.teacher_id} {self.bucket}"


@receiver(post_save, sender=Teacher)
def ensure_teacher_course_seats(sender, instance, created, **kwargs):
    if not created:
        return
    for b in CourseBucket.ALL:
        TeacherCourseSeat.objects.get_or_create(
            teacher=instance, bucket=b, defaults={"current_amount": 0, "max_amount": 5}
        )
