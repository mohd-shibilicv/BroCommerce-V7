import calendar
from io import BytesIO

import openpyxl
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from xhtml2pdf import pisa

from accounts.models import Customer
from App.models import (Category, CategoryOffers, Product, ProductImage,
                        ProductOffer, ProductSpecification,
                        ProductSpecificationValue)
from checkout.models import Coupon, DeliveryOptions
from orders.models import Invoice, Order, OrderReturn
from wallet.models import Transaction, Wallet

from .forms import (AddCouponForm, AdminOrderForm, AdminUserForm, CategoryForm,
                    CategoryOfferForm, DeliveryOptionsForm, EditProductForm,
                    EditProductImageForm, EditProductSpecificationValueForm,
                    ProductForm, ProductImageFormSet, ProductOfferForm,
                    ProductSpecificationValueFormSet)


@login_required
@staff_member_required
def shopadmin(request):
    customers = Customer.objects.all()[:5]

    # Monthly sales data
    orders_month_report = (
        Order.objects.annotate(month=ExtractMonth("created"))
        .values("month")
        .annotate(monthly_orders_count=Count("id"))
        .annotate(monthly_sales=Sum("total_paid"))
        .values("month", "monthly_orders_count", "monthly_sales")
    )
    month = []
    total_orders_per_month = []
    total_sales_per_month = []

    for order in orders_month_report:
        month.append(calendar.month_name[order["month"]])
        total_orders_per_month.append(order["monthly_orders_count"])
        total_sales_per_month.append(order["monthly_sales"])

    # Daily sales data
    current_month = timezone.now().month
    current_year = timezone.now().year
    orders_daily_report = (
        Order.objects.filter(order_status=Order.OrderStatus.PAID)
        .filter(created__month=current_month, created__year=current_year)
        .annotate(day=ExtractDay("created"))
        .values("day")
        .annotate(daily_orders_count=Count("id"))
        .annotate(daily_sales=Sum("total_paid"))
        .values("day", "daily_orders_count", "daily_sales")
    )
    day = []
    total_orders_per_day = []
    total_sales_per_day = []

    for order in orders_daily_report:
        day.append(order["day"])
        total_orders_per_day.append(order["daily_orders_count"])
        total_sales_per_day.append(order["daily_sales"])

    # Yearly sales count
    orders_year_report = (
        Order.objects.annotate(year=ExtractYear("created"))
        .values("year")
        .annotate(yearly_orders_count=Count("id"))
        .annotate(yearly_sales=Sum("total_paid"))
        .values("year", "yearly_orders_count", "yearly_sales")
    )
    year = []
    total_orders_per_year = []
    total_sales_per_year = []

    for order in orders_year_report:
        year.append(order["year"])
        total_orders_per_year.append(order["yearly_orders_count"])
        total_sales_per_year.append(order["yearly_sales"])

    orders = Order.objects.all()[:5]
    balance = Order.objects.filter(order_status=Order.OrderStatus.PAID).aggregate(
        total_sales=Sum("total_paid")
    )
    order_items = Order.objects.aggregate(order_sum=Sum("total_paid"))
    context = {
        "customers": customers,
        "orders": orders,
        "balance": balance,
        "sales": order_items,
        "month": month,
        "total_orders_per_month": total_orders_per_month,
        "total_sales_per_month": total_sales_per_month,
        "day": day,
        "total_orders_per_day": total_orders_per_day,
        "total_sales_per_day": total_sales_per_day,
        "year": year,
        "total_orders_per_year": total_orders_per_year,
        "total_sales_per_year": total_sales_per_year,
    }
    return render(request, "shopadmin/shopadmin_dashboard.html", context)


@staff_member_required
def sales_report_download_pdf(request):
    template_path = "shopadmin/sales_report_pdf_template.html"

    # Monthly sales data
    orders_month_report = (
        Order.objects.annotate(month=ExtractMonth("created"))
        .values("month")
        .annotate(monthly_orders_count=Count("id"))
        .annotate(monthly_sales=Sum("total_paid"))
        .values("month", "monthly_orders_count", "monthly_sales")
    )
    month = []
    total_orders_per_month = []
    total_sales_per_month = []

    for order in orders_month_report:
        month.append(calendar.month_name[order["month"]])
        total_orders_per_month.append(order["monthly_orders_count"])
        total_sales_per_month.append(order["monthly_sales"])

    # Daily sales data
    current_month = timezone.now().month
    current_year = timezone.now().year
    orders_daily_report = (
        Order.objects.filter(order_status=Order.OrderStatus.PAID)
        .filter(created__month=current_month, created__year=current_year)
        .annotate(day=ExtractDay("created"))
        .values("day")
        .annotate(daily_orders_count=Count("id"))
        .annotate(daily_sales=Sum("total_paid"))
        .values("day", "daily_orders_count", "daily_sales")
    )
    day = []
    total_orders_per_day = []
    total_sales_per_day = []

    for order in orders_daily_report:
        day.append(order["day"])
        total_orders_per_day.append(order["daily_orders_count"])
        total_sales_per_day.append(order["daily_sales"])

    # Yearly sales count
    orders_year_report = (
        Order.objects.annotate(year=ExtractYear("created"))
        .values("year")
        .annotate(yearly_orders_count=Count("id"))
        .annotate(yearly_sales=Sum("total_paid"))
        .values("year", "yearly_orders_count", "yearly_sales")
    )
    year = []
    total_orders_per_year = []
    total_sales_per_year = []

    for order in orders_year_report:
        year.append(order["year"])
        total_orders_per_year.append(order["yearly_orders_count"])
        total_sales_per_year.append(order["yearly_sales"])

    context = {
        "month": month,
        "total_orders_per_month": total_orders_per_month,
        "total_sales_per_month": total_sales_per_month,
        "day": day,
        "total_orders_per_day": total_orders_per_day,
        "total_sales_per_day": total_sales_per_day,
        "year": year,
        "total_orders_per_year": total_orders_per_year,
        "total_sales_per_year": total_sales_per_year,
        "monthly_sales": zip(month, total_orders_per_month, total_sales_per_month),
        "daily_sales": zip(day, total_orders_per_day, total_sales_per_day),
        "yearly_sales": zip(year, total_orders_per_year, total_sales_per_year),
    }

    # Create a Django response object with appropriate PDF headers
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="sales_report.pdf"'

    # Create a PDF object, using the response object as its "file."
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If the PDF creation failed, return an error response.
    if pisa_status.err:
        return HttpResponse(
            "We had some errors with code %s <pre>%s</pre>" % (pisa_status.err, html)
        )

    return response


@staff_member_required
def sales_report_download_excel(request):
    # Monthly sales data
    orders_month_report = (
        Order.objects.annotate(month=ExtractMonth("created"))
        .values("month")
        .annotate(monthly_orders_count=Count("id"))
        .annotate(monthly_sales=Sum("total_paid"))
        .values("month", "monthly_orders_count", "monthly_sales")
    )
    month = []
    total_orders_per_month = []
    total_sales_per_month = []

    for order in orders_month_report:
        month.append(calendar.month_name[order["month"]])
        total_orders_per_month.append(order["monthly_orders_count"])
        total_sales_per_month.append(order["monthly_sales"])

    # Daily sales data
    current_month = timezone.now().month
    current_year = timezone.now().year
    orders_daily_report = (
        Order.objects.filter(order_status=Order.OrderStatus.PAID)
        .filter(created__month=current_month, created__year=current_year)
        .annotate(day=ExtractDay("created"))
        .values("day")
        .annotate(daily_orders_count=Count("id"))
        .annotate(daily_sales=Sum("total_paid"))
        .values("day", "daily_orders_count", "daily_sales")
    )
    day = []
    total_orders_per_day = []
    total_sales_per_day = []

    for order in orders_daily_report:
        day.append(order["day"])
        total_orders_per_day.append(order["daily_orders_count"])
        total_sales_per_day.append(order["daily_sales"])

    # Yearly sales count
    orders_year_report = (
        Order.objects.annotate(year=ExtractYear("created"))
        .values("year")
        .annotate(yearly_orders_count=Count("id"))
        .annotate(yearly_sales=Sum("total_paid"))
        .values("year", "yearly_orders_count", "yearly_sales")
    )
    year = []
    total_orders_per_year = []
    total_sales_per_year = []

    for order in orders_year_report:
        year.append(order["year"])
        total_orders_per_year.append(order["yearly_orders_count"])
        total_sales_per_year.append(order["yearly_sales"])

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = "attachment; filename=sales_report_brocommerce.xlsx"

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Add your daily data to the worksheet
    worksheet.append(["Date", "Total Orders", "Total Sales"])
    for d, orders, sales in zip(day, total_orders_per_day, total_sales_per_day):
        worksheet.append([d, orders, sales])
    # Add your monthly data to the worksheet
    worksheet.append(["Month", "Total Orders", "Total Sales"])
    for m, orders, sales in zip(month, total_orders_per_month, total_sales_per_month):
        worksheet.append([m, orders, sales])
    # Add your yearly data to the worksheet
    worksheet.append(["Year", "Total Orders", "Total Sales"])
    for y, orders, sales in zip(year, total_orders_per_year, total_sales_per_year):
        worksheet.append([y, orders, sales])

    workbook.save(response)

    return response


@login_required
@staff_member_required
def customers(request):
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "shopadmin/customers.html", context)


@login_required
@staff_member_required
def activate_or_deactivate_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    if customer.is_active:
        customer.is_active = False
        messages.info(request, f"{customer} deactivated")
        customer.save()
    else:
        customer.is_active = True
        messages.info(request, f"{customer} activated")
        customer.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@staff_member_required
def orders(request):
    orders = Order.objects.all()
    sort_param = request.GET.get("sort")

    if sort_param == "default":
        orders = orders.order_by("-created")
    elif sort_param == "paid":
        orders = orders.filter(order_status=Order.OrderStatus.PAID).order_by("-created")
    elif sort_param == "pending":
        orders = orders.filter(order_status=Order.OrderStatus.PENDING).order_by(
            "-created"
        )
    elif sort_param == "cancelled":
        orders = orders.filter(order_status=Order.OrderStatus.CANCELLED).order_by(
            "-created"
        )
    elif sort_param == "returned":
        orders = orders.filter(order_status=Order.OrderStatus.RETURNED).order_by(
            "-created"
        )

    orders_per_page = 10
    paginator = Paginator(orders, orders_per_page)
    page_number = request.GET.get("page")
    orders_on_page = paginator.get_page(page_number)

    context = {"orders": orders_on_page, "sort_param": sort_param}
    return render(request, "shopadmin/orders/orders.html", context)


@login_required
@staff_member_required
def view_order_details(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == "POST":
        order_form = AdminOrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_status = order_form.cleaned_data["order_status"]
            order_form.save(commit=False)
            if order_status == Order.OrderStatus.CANCELLED:
                wallet = Wallet.objects.get(user=order.user)
                final_balance = float(wallet.balance) + float(order.total_paid)
                wallet.balance = final_balance
                wallet.save()

                for item in order.items.all():
                    product = item.product
                    product.product_stock += item.quantity  # Increment product stock
                    product.save()

                Transaction.objects.create(
                    user=order.user,
                    transaction_type=Transaction.TransactionTypes.RETURN,
                    amount=float(order.total_paid),
                )

                order.delivery_status = Order.DeliveryStatus.REJECTED
                order.order_status = Order.OrderStatus.RETURNED
                order.save()
                order_form.save()
                messages.success(request, f"Order {order.order_key} updated")
                return redirect("shopadmin:orders")
            order_form.save()
            messages.success(request, f"Order {order.order_key} updated")
            return redirect("shopadmin:orders")
    else:
        order_form = AdminOrderForm(instance=order)

    context = {
        "order": order,
        "order_form": order_form,
    }
    return render(request, "shopadmin/orders/order_details.html", context)


@login_required
@staff_member_required
def return_requests(request):
    return_requests = OrderReturn.objects.all().order_by("-date")
    return render(
        request,
        "shopadmin/orders/return_requests.html",
        {"return_requests": return_requests},
    )


@login_required
@staff_member_required
def return_order_details(request, id):
    return_request = get_object_or_404(OrderReturn, pk=id)
    order = Order.objects.get(pk=return_request.order.id)
    refund_amount = float(order.total_paid) * 0.8

    if request.method == "POST":
        wallet = Wallet.objects.get(user=return_request.user)
        final_balance = float(wallet.balance) + refund_amount
        wallet.balance = final_balance
        wallet.save()

        for item in order.items.all():
            product = item.product
            product.product_stock += item.quantity  # Increment product stock
            product.save()

        Transaction.objects.create(
            user=return_request.user,
            transaction_type=Transaction.TransactionTypes.RETURN,
            amount=refund_amount,
        )

        order.order_status = Order.OrderStatus.RETURNED
        order.delivery_status = Order.DeliveryStatus.REJECTED
        order.save()

        return_request.approved = True
        return_request.save()

        messages.success(
            request,
            "Order is returned and the refund amount were added to user's wallet",
        )
        return HttpResponseRedirect(reverse("shopadmin:return_requests"))

    context = {"return_request": return_request}
    return render(request, "shopadmin/orders/return_order_details.html", context)


@login_required
@staff_member_required
def invoices(request):
    invoices = Invoice.objects.all().order_by("-issued_date")
    context = {"invoices": invoices}
    return render(request, "shopadmin/invoices.html", context)


@login_required
@staff_member_required
def categories(request):
    categories = Category.objects.filter()
    context = {"categories": categories}
    return render(request, "shopadmin/categories/categories.html", context)


@login_required
@staff_member_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added")
            return redirect("shopadmin:categories")
    else:
        form = CategoryForm()
    return render(request, "shopadmin/categories/add_category.html", {"form": form})


@login_required
@staff_member_required
def edit_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category {category.name} updated")
            return redirect("shopadmin:categories")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "shopadmin/categories/edit_category.html",
        {"form": form, "category": category},
    )


def edit_category_offers(request, category_slug):
    category_offer = CategoryOffers.objects.filter(
        category__slug=category_slug,
    ).first()

    form = CategoryOfferForm(instance=category_offer)
    if request.method == "POST":
        form = CategoryOfferForm(request.POST, instance=category_offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Categroy offer updated")
            return redirect("shopadmin:categories")

    context = {"form": form}
    return render(request, "shopadmin/categories/edit_category_offers.html", context)


@login_required
@staff_member_required
def activate_or_deactivate_category(request, id):
    category = get_object_or_404(Category, pk=id)
    if category.is_active:
        category.is_active = False
        messages.info(request, f"{category} deactivated")
        category.save()
    else:
        category.is_active = True
        messages.info(request, f"{category} activated")
        category.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def products(request):
    products = Product.objects.all()

    sort_param = request.GET.get("sort", "default")  # Default sorting

    if sort_param == "title":
        products = products.order_by("title")
    elif sort_param == "price":
        products = products.order_by("discount_price")
    elif sort_param == "publication_date":
        products = products.order_by("-created_at")

    products_per_page = 8
    paginator = Paginator(products, products_per_page)
    page_number = request.GET.get("page")
    products_on_page = paginator.get_page(page_number)

    context = {"products": products_on_page, "sort_param": sort_param}
    return render(request, "shopadmin/products/products.html", context)


@login_required
@staff_member_required
def add_product(request):
    specifications = ProductSpecification.objects.all()

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        image_formset = ProductImageFormSet(
            request.POST, request.FILES, queryset=ProductImage.objects.none()
        )
        spec_value_formset = ProductSpecificationValueFormSet(request.POST)

        if (
            product_form.is_valid()
            and image_formset.is_valid()
            and spec_value_formset.is_valid()
        ):
            product = product_form.save()

            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

                    # Crop the image if crop coordinates are provided
                    left = image_form.cleaned_data.get('crop_left')
                    right = image_form.cleaned_data.get('crop_right')
                    upper = image_form.cleaned_data.get('crop_upper')
                    lower = image_form.cleaned_data.get('crop_lower')
                    print(f'{left}, {upper}, {right}, {lower}')
                    if left and right and upper and lower:
                        try:
                            img = Image.open(image.image)
                            left = image_form.cleaned_data.get('crop_left')
                            right = image_form.cleaned_data.get('crop_right')
                            upper = image_form.cleaned_data.get('crop_upper')
                            lower = image_form.cleaned_data.get('crop_lower')
                            if 0 <= left <= right <= img.width and 0 <= upper <= lower <= img.height:
                                cropped_img = img.crop((left, upper, right, lower))
                                buffer = BytesIO()
                                cropped_img.save(buffer, format='JPEG')
                                image.image.save(f'cropped_{image.image.name}', ContentFile(buffer.getvalue()))
                            else:
                                # Handle the case where cropping coordinates are out of bounds
                                messages.info(request, 'Invalid cropping coordinates.')
                                return redirect('shopadmin:products')
                        except Exception as e:
                            print(f"An error occurred while cropping the image: {str(e)}")
                            messages.info(request, 'An error occurred while processing the image.')
                            return redirect('shopadmin:products')
                    else:
                        messages.info(request, 'Missing cropping coordinates.')
                        return redirect('shopadmin:products')

            messages.success(request, "Product added")
            return redirect("shopadmin:products")
    else:
        product_form = ProductForm()
        image_formset = ProductImageFormSet(queryset=ProductImage.objects.none())
        spec_value_formset = ProductSpecificationValueFormSet(
            queryset=ProductSpecificationValue.objects.none()
        )

    return render(
        request,
        "shopadmin/products/add_product.html",
        {
            "product_form": product_form,
            "image_formset": image_formset,
            "spec_value_formset": spec_value_formset,
            "specifications": specifications,
        },
    )


@login_required
@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        edit_form = EditProductForm(request.POST, request.FILES, instance=product)

        if edit_form.is_valid():
            edit_form.save()

            messages.success(request, "Product updated")
            return redirect("shopadmin:products")
    else:
        edit_form = EditProductForm(instance=product)

    specifications = ProductSpecification.objects.all()

    return render(
        request,
        "shopadmin/products/edit_product.html",
        {
            "edit_form": edit_form,
            "product": product,
            "specifications": specifications,
        },
    )


@login_required
@staff_member_required
def edit_specification_values(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    specifications = ProductSpecification.objects.all()

    if request.method == "POST":
        SpecificationValueFormSet = modelformset_factory(
            ProductSpecificationValue,
            form=EditProductSpecificationValueForm,
            extra=3,
            max_num=3,
            min_num=1,
        )
        formset = SpecificationValueFormSet(
            request.POST,
            queryset=ProductSpecificationValue.objects.filter(product=product),
        )

        if formset.is_valid():
            formset.save()
            messages.success(request, "Product specification values updated")
            return redirect("shopadmin:products")
    else:
        SpecificationValueFormSet = modelformset_factory(
            ProductSpecificationValue,
            form=EditProductSpecificationValueForm,
            extra=3,
            max_num=3,
            min_num=1,
        )
        formset = SpecificationValueFormSet(
            queryset=ProductSpecificationValue.objects.filter(product=product)
        )

    return render(
        request,
        "shopadmin/products/edit_specification_values.html",
        {
            "formset": formset,
            "product": product,
            "specifications": specifications,
        },
    )


@login_required
@staff_member_required
def edit_product_images(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    specifications = ProductSpecification.objects.all()

    if request.method == "POST":
        ImageFormSet = modelformset_factory(
            ProductImage,
            form=EditProductImageForm,
            extra=3,
            max_num=4,
            min_num=1,
        )
        formset = ImageFormSet(
            request.POST,
            request.FILES,
            queryset=ProductImage.objects.filter(product=product),
        )
        if formset.is_valid():
            for image_form in formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

                    # Crop the image if crop coordinates are provided
                    left = image_form.cleaned_data.get("crop_left")
                    right = image_form.cleaned_data.get("crop_right")
                    upper = image_form.cleaned_data.get("crop_upper")
                    lower = image_form.cleaned_data.get("crop_lower")

                    if left and right and upper and lower:
                        try:
                            img = Image.open(image.image)
                            if (0 <= left <= right <= img.width and 0 <= upper <= lower <= img.height):
                                cropped_img = img.crop((left, upper, right, lower))
                                buffer = BytesIO()
                                cropped_img.save(buffer, format="JPEG")
                                image.image.save(
                                    f"cropped_{image.image.name}",
                                    ContentFile(buffer.getvalue()),
                                )
                            else:
                                messages.info(
                                    request,
                                    "Invalid cropping coordinates for one or more images.",
                                )
                                return redirect("shopadmin:products")
                        except Exception as e:
                            print(
                                f"An error occurred while cropping an image: {str(e)}"
                            )
                            messages.info(
                                request,
                                "An error occurred while processing one or more images.",
                            )
                            return redirect("shopadmin:products")

            messages.success(request, "Product images updated")
            return redirect("shopadmin:products")
        else:
            # Debugging: Print the errors in the formset to understand what might be wrong
            print(formset.errors)
    else:
        ImageFormSet = modelformset_factory(
            ProductImage,
            form=EditProductImageForm,
            extra=3,
            max_num=4,
            min_num=1,
        )
        formset = ImageFormSet(queryset=ProductImage.objects.filter(product=product))

    return render(
        request,
        "shopadmin/products/edit_product_images.html",
        {
            "formset": formset,
            "product": product,
            "specifications": specifications,
        },
    )


@login_required
@staff_member_required
def edit_product_offer(request, product_id):
    product_offer = ProductOffer.objects.filter(product__id=product_id).first()

    form = ProductOfferForm(instance=product_offer)
    if request.method == "POST":
        form = ProductOfferForm(request.POST, instance=product_offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Product offer updated")
            return redirect("shopadmin:products")

    return render(request, "shopadmin/products/edit_product_offer.html", {"form": form})


@login_required
@staff_member_required
def delete_image(request):
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        try:
            image = ProductImage.objects.get(pk=image_id)
            image.delete()
            return JsonResponse({"success": True})
        except ProductImage.DoesNotExist:
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})


@login_required
@staff_member_required
def activate_or_deactivate_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.is_active:
        product.is_active = False
        messages.info(request, f"{product} deactivated")
        product.save()
    else:
        product.is_active = True
        messages.info(request, f"{product} activated")
        product.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def admins(request):
    admins = Customer.objects.filter(is_staff=True)
    context = {"admins": admins}
    return render(request, "shopadmin/admins/admins.html", context)


@login_required
@staff_member_required
def add_admin_user(request):
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_active = form.cleaned_data.get("is_active")
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("shopadmin:admins")
    else:
        form = AdminUserForm()

    return render(request, "shopadmin/admins/add_admin.html", context={"form": form})


@login_required
@staff_member_required
def activate_or_deactivate_admin(request, admin_id):
    admin = Customer.objects.get(pk=admin_id, is_staff=True)
    if admin.is_active:
        admin.is_active = False
        messages.info(request, f"{admin} deactivated")
        admin.save()
    else:
        admin.is_active = True
        messages.info(request, f"{admin} activated")
        admin.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def profile(request):
    admin = Customer.objects.get(pk=request.user.id)
    context = {"admin": admin}
    return render(request, "shopadmin/shopadmin_profile.html", context)


def admin_search_products(request):
    if request.method == "POST":
        query = request.POST["search"]

        products = Product.objects.filter(
            Q(title__icontains=query)
            | Q(category__name__icontains=query)
            | Q(product_type__name__icontains=query)
        )

        products_per_page = 20
        paginator = Paginator(products, products_per_page)
        page_number = request.GET.get("page")
        products_on_page = paginator.get_page(page_number)

        return render(
            request,
            "shopadmin/products/products.html",
            context={"query": query, "products": products_on_page},
        )

    return render(request, "shopadmin/products/products.html")


@login_required
@staff_member_required
def delivery_options(request):
    delivery_options = DeliveryOptions.objects.all()
    context = {"delivery_options": delivery_options}
    return render(request, "shopadmin/delivery_options.html", context)


@login_required
@staff_member_required
def create_delivery_option(request):
    form = DeliveryOptionsForm()
    if request.method == "POST":
        form = DeliveryOptionsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Delivery Option Added")
            return redirect("shopadmin:delivery_options")

    context = {"form": form}
    return render(request, "shopadmin/create_delivery_option.html", context)


@login_required
@staff_member_required
def edit_delivery_option(request, id):
    delivery_option = get_object_or_404(DeliveryOptions, pk=id)
    form = DeliveryOptionsForm(instance=delivery_option)
    if request.method == "POST":
        form = DeliveryOptionsForm(request.POST, instance=delivery_option)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery Option updated")
            return redirect("shopadmin:delivery_options")

    context = {"form": form}
    return render(request, "shopadmin/edit_delivery_option.html", context)


@login_required
@staff_member_required
def delete_delivery_option(request, id):
    delivery_option = get_object_or_404(DeliveryOptions, pk=id)
    delivery_option.delete()
    messages.success(request, f"Delivery option {delivery_option} deleted")
    return redirect("shopadmin:delivery_options")


@login_required
@staff_member_required
def coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'shopadmin/coupon/coupons.html', {'coupons': coupons})


@login_required
@staff_member_required
def add_coupon(request):
    form = AddCouponForm()
    if request.method == 'POST':
        form = AddCouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon added')
            return redirect('shopadmin:coupons')

    return render(request, 'shopadmin/coupon/add_coupon.html', {'form': form})


@login_required
@staff_member_required
def coupon_activate_or_deactivate(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if coupon.active:
        coupon.active = False
        coupon.save()
        messages.info(request, 'Coupon deactivated')
    else:
        coupon.active = True
        coupon.save()
        messages.info(request, 'Coupon activated')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@staff_member_required
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)

    form = AddCouponForm(instance=coupon)
    if request.method == 'POST':
        form = AddCouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.info(request, f'Coupon {coupon.code} updated')
            return redirect('shopadmin:coupons')

    return render(request, 'shopadmin/coupon/edit_coupon.html', {'form': form})
