from django.urls import path
from task_manager.tasks import views


app_name = 'tasks'

urlpatterns = [
    path('', views.TasksList.as_view(), name='tasks'),
    path('create/', views.CreateTask.as_view(), name='create_task'),
    path('<int:pk>', views.ShowTask.as_view(), name='show_task'),
    path('<int:pk>/update/', views.UpdateTask.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(), name='delete_task'),
]
