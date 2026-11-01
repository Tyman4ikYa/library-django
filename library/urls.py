from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_view, name='book_list'),
    path('books/', views.book_list_view, name='book_list'),
    path('books/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('authors/', views.author_list_view, name='author_list'),
    path('authors/<int:pk>/', views.author_detail_view, name='author_detail'),
    path('readers/', views.reader_list_view, name='reader_list'),
    path('readers/<int:pk>/', views.reader_detail_view, name='reader_detail'),
    path('about/', views.about_view, name='about'),
]