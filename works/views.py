from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView

from users.models import Teacher, Group, Student, InformationAboutTheNumberOfSeats
from works.forms import AddStudent, WorkForm
from works.models import Work


class SearchWorksView(ListView):
    
    model = Work
    template_name = 'works/home.html'
    extra_context = {
        'title': 'Архив работ',
    }

    def get_queryset(self): # новый
        query = self.request.GET.get('q')

        if query != None:
            object_list = Work.objects.filter(
                Q(name__icontains=query)
            )
            return object_list
        else:
            return Work.objects.all()


class ShowTeachersView(ListView):
    model = Teacher
    template_name = 'works/list_teachers.html'

    extra_context = {'faculty': Teacher.DEPARTMENT_CHOICES, 'teachers':
        Teacher.objects.all(), 'number_of_seats': InformationAboutTheNumberOfSeats.objects.all()}

    def get_queryset(self): # новый
        query = self.request.GET.get('q')

        if query != None:
            object_list = Work.objects.filter(
                Q(name__icontains=query)
            )
            return object_list
        else:
            return Work.objects.all()

    # def form_valid(self, form):
    #     w = form.save(commit=False)
    #     w.author = self.request.user
    #     return super().form_valid(form)


class ShowStudentsView(ListView):
    model = Student
    template_name = 'works/add_student.html'

    extra_context = {'students':
        Student.objects.all(),
                     'teachers': Teacher.objects.all()}

    def get_queryset(self): # новый
        query = self.request.GET.get('q')

        if query != None:
            object_list = Student.objects.filter(
                Q(user__first_name__icontains=query)
            )
            return object_list
        else:
            return Student.objects.all()

    # def add_student(request):
    #
    #     if request.method == 'POST':
    #         user_form = AddStudent(request.POST, instance=request.user)
    #
    #         if user_form.is_valid():
    #             user_form.save()
    #             # redirect('home')
    #
    #         else:
    #             pass
    #             # message.error
    #     user_form = AddStudent(instance=request.user)
    #
    #     return render(request, 'works/add_student.html', {
    #         'user_form': user_form,
    #     })


def check_works(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        student = Student.objects.get(id=request.POST.get('student_id'))
        student.scientific_director = teacher
        student.save()
        work = Work(
            author=student,
            scientific_director=teacher,
            is_completed=False
        )
        work.save()

    students = Student.objects.filter(scientific_director=teacher)
    works = []
    for student in students:
        if student.scientific_director == teacher:
            works.append(Work.objects.get(author=student))

    return render(request, 'works/check_works.html', {
        'students': students,
        'works': works
    })


def write_work(request):
    work = Work.objects.get(author=request.user.student)
    if request.method == 'POST':
        work_form = WorkForm(request.POST, instance=work)

        if work_form.is_valid():
            work_form.save()
            return redirect('home')

        else:
            pass
            # message.error
    # user_form = UserForm(instance=request.user)
    # if is_teacher:
    #     profile_form = TeacherForm(instance=profile)
    # else:
    #     profile_form = StudentForm(instance=profile)

    work_form = WorkForm(instance=work)
    student = Student.objects.get(user=request.user)
    works = Work.objects.filter(author=student)

    return render(request, 'works/write_work.html', {
        'work_form': work_form,
        'student': student,
        'works': works
    })
