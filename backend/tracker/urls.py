from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("api/get-categories/", views.CategoryListView.as_view(), name="get_categories"),
    path("api/get-subcategories/", views.SubcategoryListView.as_view(), name="get_subcategories"),
]
