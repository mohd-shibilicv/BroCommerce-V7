from datetime import date, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from accounts.models import Address
from App_cart.cart import Cart
from wallet.models import Transaction, Wallet

from .forms import OrderReturnForm
from .models import Invoice, Order, OrderItem, OrderReturn


def add(request):
    basket = Cart(request)
    print(request.POST)
    if request.POST.get("action") == "post":
        order_key = request.POST.get("order_key")
        user_id = request.user.id
        baskettotal = basket.get_total_price()
        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["qty"],
                )

        # Return a JSON response
        response_data = {"success": "Order successfully created"}
        return JsonResponse(response_data)

    # Handle other cases if needed
    return JsonResponse({"error": "Invalid request"})


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def order_return(request, order_id):
    order = Order.objects.get(id=order_id)
    return_request = OrderReturn.objects.get(order=order)
    total_paid = order.total_paid
    refund_amount = float(order.total_paid) * 0.8

    if request.method == "POST":
        form = OrderReturnForm(request.POST)
        if form.is_valid():
            wallet = Wallet.objects.get(user=request.user)
            final_balance = float(wallet.balance) + refund_amount
            wallet.balance = final_balance
            wallet.save()

            for item in order.items.all():
                product = item.product
                product.product_stock += item.quantity  # Increment product stock
                product.save()

            Transaction.objects.create(
                user=request.user,
                transaction_type=Transaction.TransactionTypes.RETURN,
                amount=refund_amount,
            )

            order.order_status = Order.OrderStatus.RETURNED
            order.delivery_status = Order.DeliveryStatus.REJECTED
            order.save()

            return_request.approved = True
            return_request.save()

            if "return_requests" in request.META.get("HTTP_REFERER"):
                messages.success(
                    request,
                    "Order is returned and the refund amount were added to user's wallet",
                )
                return HttpResponseRedirect(reverse("shopadmin:return_requests"))

            messages.success(
                request,
                "Order is returned and the refund amount were added to your wallet",
            )
            return redirect("account:user_orders")
    else:
        form = OrderReturnForm()

    context = {"form": form, "total_paid": total_paid, "refund_amount": refund_amount}
    return render(request, "orders/return_order.html", context)


def generate_unique_invoice_number():
    today = date.today()
    year = today.strftime("%Y")

    last_invoice = (
        Invoice.objects.filter(invoice_number__startswith=year)
        .order_by("-invoice_number")
        .first()
    )

    if last_invoice:
        last_invoice_number = last_invoice.invoice_number
        last_counter = int(last_invoice_number.split("-")[-1])
    else:
        last_counter = 0

    new_counter = last_counter + 1
    invoice_number = f"{year}-{new_counter:04d}"

    return invoice_number


def generate_invoice(request, order_id):
    order = Order.objects.get(pk=order_id)
    customer = request.user
    invoice_number = generate_unique_invoice_number()

    do_invoice_exists = Invoice.objects.filter(order=order).exists()
    if not do_invoice_exists:
        invoice = Invoice(
            invoice_number=invoice_number,
            order=order,
            customer=customer,
            issued_date=order.created,
            due_date=order.created + timedelta(days=30),
            total_amount=order.total_paid,
        )
        invoice.save()
    else:
        invoice = Invoice.objects.get(order=order)

    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=invoice_{invoice_number}.pdf"

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Invoice #{invoice_number}")
    p.drawString(100, 730, f'Order Date: {order.created.strftime("%Y-%m-%d %H:%M:%S")}')
    p.drawString(100, 710, f'Due Date: {invoice.due_date.strftime("%Y-%m-%d")}')
    p.drawString(100, 690, f"Total Amount: {invoice.total_amount}")

    # Table for displaying order items
    data = [["Title", "Price", "Quantity", "Total"]]
    for item in order.items.all():
        data.append(
            [item.product.title, item.price, item.quantity, item.get_total_price()]
        )

    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table.wrapOn(p, 0, 0)
    table.drawOn(p, 100, 600)

    p.showPage()
    p.save()
    return response


def invoices(request):
    invoices = Invoice.objects.filter(customer=request.user).order_by("-issued_date")
    invoices_per_page = 10
    paginator = Paginator(invoices, invoices_per_page)
    page_number = request.GET.get("page")
    invoices_on_page = paginator.get_page(page_number)
    context = {"invoices": invoices_on_page}
    return render(request, "orders/invoices.html", context)


def invoice_details(request, id):
    invoice = Invoice.objects.get(pk=id)
    address = Address.objects.get(customer=request.user, default=True)
    context = {"invoice": invoice, "address": address}
    return render(request, "orders/invoice_details.html", context)


def delete_invoice(request, id):
    invoice = Invoice.objects.get(pk=id)
    invoice.delete()
    messages.success(request, f"Invoice #{invoice.invoice_number} deleted successfully")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
