from django.db.models import Q
from django.views.generic import ListView

from users.models import Teacher
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
        Teacher.objects.all()}

    # def get_queryset(self): # новый
    #     query = self.request.GET.get('q')
    #
    #     if query != None:
    #         object_list = Work.objects.filter(
    #             Q(name__icontains=query)
    #         )
    #         return object_list
    #     else:
    #         return Work.objects.all()