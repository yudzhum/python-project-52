from django.urls import path
from task_manager.users import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersList.as_view(), name='users'),
    path('create/', views.RegisterUser.as_view(), name="register"),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name="update_user"),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name="delete_user")
]
