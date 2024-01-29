from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'), # Add this line
    path('select/', views.select_books, name='select_books'),
    path('selected/', views.selected_books, name='selected_books'),
    path('booklist/', views.book_list, name='book_list'), # Add this line
    path('logout/', views.user_logout, name='user_logout'), # Add this line
    path('register/', views.register, name='register'), # Add this line
    path('deselect/', views.deselect_books, name='deselect_books'), # Add this line
]
