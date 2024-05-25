from django.urls import path

from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('logout/', auth_view.LogoutView.as_view(next_page='index'), name='logout'),
]
