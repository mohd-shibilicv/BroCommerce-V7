from django.urls import path

from . import views

app_name = "App"

urlpatterns = [
    path("", views.all_products, name="all_products"),
    path("<slug:slug>", views.product_details, name="product_details"),
    path("delete_review/<int:id>/", views.delete_review, name="delete_review"),
    path("like_comment/", views.like_comment, name="like_comment"),
    path("shop/<slug:category_slug>", views.category_list, name="category_list"),
    path("search/", views.search_products, name="search"),
    path('export/', views.export_data, name='export_data'),
]
