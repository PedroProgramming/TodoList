from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('usuarios/', views.user_system, name="user_system"),
    path('view_user/<int:id_user>', views.view_user, name="view_user"),
    path('delete_user/<int:id>', views.delete_user, name="deletar_user"),
    path('edit_user/<int:id>', views.edit_user, name="edit_user"),
]
