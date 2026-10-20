from django.urls import path
from . import views

app_name = "borrowings"

urlpatterns = [
    path("create/", views.borrowing_create_view, name="create"),
    path("", views.borrowing_list_view, name="list"),
    path("<int:pk>/", views.borrowing_detail_view, name="detail"),
    path("<int:pk>/return/", views.borrowing_return_view, name="return"),
]