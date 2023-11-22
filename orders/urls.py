from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("add/", views.add, name="add-order"),
    path("invoices/", views.invoices, name="invoices"),
    path("invoice_details/<int:id>/", views.invoice_details, name="invoice_details"),
    path("delete_invoice/<int:id>/", views.delete_invoice, name="delete_invoice"),
    path("order_return/<int:order_id>/", views.order_return, name="order_return"),
    path(
        "generate_invoice/<int:order_id>/",
        views.generate_invoice,
        name="generate_invoice",
    ),
]
