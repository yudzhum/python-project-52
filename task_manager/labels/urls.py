from django.urls import path
from task_manager.labels import views


app_name = 'labels'

urlpatterns = [
    path('', views.ShowLabels.as_view(), name='labels'),
    path('create/', views.CreateLabel.as_view(), name='create_label'),
    path('<int:pk>/update/', views.UpdateLabel.as_view(), name='update_label'),
    path('<int:pk>/delete/', views.DeleteLabel.as_view(), name='delete_label'),
]
