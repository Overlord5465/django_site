from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.SearchWorksView.as_view(), name='home'),  # http://127.0.0.1:8000
    path('list_teacher/', views.ShowTeachersView.as_view(), name='list_teacher'),
    # path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
]