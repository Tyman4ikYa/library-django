from django.urls import path
from . import views

app_name = "reading"

urlpatterns = [
    path("", views.reading_list_detail_view, name="detail"),
    path("add/<int:book_id>/", views.add_to_reading_view, name="add"),
    path("update/<int:item_id>/", views.update_reading_item_view, name="update"),
    path("remove/<int:item_id>/", views.remove_reading_item_view, name="remove"),
]