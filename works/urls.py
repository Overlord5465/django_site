from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchWorksView.as_view(), name='home'),
    path('list_teacher/', views.ShowTeachersView.as_view(), name='list_teacher'),
    path('add_student/', views.ShowStudentsView.as_view(), name='add_student'),
    path('check_works/', views.check_works, name='check_works'),
    path('write_work/', views.write_work, name='write_work'),
]
