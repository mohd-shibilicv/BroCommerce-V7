from django.urls import path

from . import views

app_name = "shopadmin"

urlpatterns = [
    path("", views.shopadmin, name="shopadmin"),
    path("invoices/", views.invoices, name="invoices"),
    path("profile/", views.profile, name="profile"),
    path("search/", views.admin_search_products, name="search"),
    path(
        "sales_report_download_pdf/",
        views.sales_report_download_pdf,
        name="sales_report_download_pdf",
    ),
    path(
        "sales_report_download_excel/",
        views.sales_report_download_excel,
        name="sales_report_download_excel",
    ),
    path("delivery_options/", views.delivery_options, name="delivery_options"),
    path(
        "create_delivery_option/",
        views.create_delivery_option,
        name="create_delivery_option",
    ),
    path(
        "edit_delivery_option/<int:id>/",
        views.edit_delivery_option,
        name="edit_delivery_option",
    ),
    path(
        "delete_delivery_option/<int:id>/",
        views.delete_delivery_option,
        name="delete_delivery_option",
    ),
    # Orders URLs
    path("orders/", views.orders, name="orders"),
    path(
        "view_order_details/<int:id>/",
        views.view_order_details,
        name="view_order_details",
    ),
    path("return_requests/", views.return_requests, name="return_requests"),
    path(
        "return_order_details/<int:id>/",
        views.return_order_details,
        name="return_order_details",
    ),
    # Customers URLs
    path("customers/", views.customers, name="customers"),
    path(
        "activate_or_deactivate_customer/<int:id>/",
        views.activate_or_deactivate_customer,
        name="activate_or_deactivate_customer",
    ),
    # Admins URLs
    path("admins/", views.admins, name="admins"),
    path("add_admin/", views.add_admin_user, name="add_admin"),
    path(
        "activate_or_deactivate_admin/<int:admin_id>/",
        views.activate_or_deactivate_admin,
        name="activate_or_deactivate_admin",
    ),
    # Categories URLs
    path("categories/", views.categories, name="categories"),
    path("categories/add/", views.add_category, name="add_category"),
    path(
        "edit-category/<slug:category_slug>/", views.edit_category, name="edit_category"
    ),
    path(
        "edit-category-offer/<slug:category_slug>/",
        views.edit_category_offers,
        name="edit_category_offers",
    ),
    path(
        "activate_or_deactivate_category/<int:id>/",
        views.activate_or_deactivate_category,
        name="activate_or_deactivate_category",
    ),
    # Products URLs
    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path(
        "products/edit-specifications/<int:product_id>/",
        views.edit_specification_values,
        name="edit_specification_values",
    ),
    path(
        "products/edit_product_offer/<int:product_id>/",
        views.edit_product_offer,
        name="edit_product_offer",
    ),
    path(
        "products/edit-images/<int:product_id>/",
        views.edit_product_images,
        name="edit_product_images",
    ),
    path("delete_image/", views.delete_image, name="delete_image"),
    path(
        "activate_or_deactivate_product/<int:id>/",
        views.activate_or_deactivate_product,
        name="activate_or_deactivate_product",
    ),
    # Coupon URLs
    path("coupons/", views.coupons, name="coupons"),
    path("add_coupon/", views.add_coupon, name="add_coupon"),
    path(
        "coupon_activate_or_deactivate/<int:coupon_id>/",
        views.coupon_activate_or_deactivate,
        name="coupon_activate_or_deactivate",
    ),
    path("edit_coupon/<int:coupon_id>/", views.edit_coupon, name="edit_coupon"),
]
