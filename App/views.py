from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from wallet.models import Wallet

from .filters import ProductFilter
from .forms import ProductReviewForm
from .models import Category, Product, ProductReview, ProductSpecificationValue
from .resources import ProductModelResource


def all_products(request):
    products = (
        Product.objects.prefetch_related("product_image")
        .select_related("category").prefetch_related("product_offer")
        .filter(is_active=True)
    )

    sort_param = request.GET.get("sort", "default")

    if sort_param == "title":
        products = products.order_by("title")
    elif sort_param == "price":
        products = products.order_by("discount_price")
    elif sort_param == "publication_date":
        products = products.order_by("-created_at")

    products_filter = ProductFilter(request.GET, queryset=products)
    product_filter_form = products_filter.form
    products_filter_queryset = products_filter.qs

    products_per_page = 8
    paginator = Paginator(products_filter_queryset, products_per_page)
    page_number = request.GET.get("page")
    products_on_page = paginator.get_page(page_number)

    context = {
        "products": products_on_page,
        "sort_param": sort_param,
        "filter_form": product_filter_form,
    }
    return render(request, "App/index.html", context)


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_specifications = ProductSpecificationValue.objects.filter(product=product)
    images = product.get_images()
    related_products = (
        Product.objects.filter(
            category__in=Category.objects.get(
                slug=product.category.slug
            ).get_descendants(include_self=True)
        )
        .filter(category__in=Category.objects.filter(slug=product.category.slug), is_active=True)
        .exclude(title=product.title)
    )
    default_products = Product.objects.filter(is_active=True)[6:10]

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.review_profile = request.user.profile
            review.reviewer_name = request.user.username
            review.reviewer_email = request.user.email
            review.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = ProductReviewForm()

    reviews = product.reviews.all()[:10]

    context = {
        "product": product,
        "related_products": related_products,
        "default_products": default_products,
        "images": images,
        "product_specifications": product_specifications,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "App/products/product_details.html", context)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(
            include_self=True
        )
    )
    sort_param = request.GET.get("sort", "default")

    if sort_param == "title":
        products = products.order_by("title")
    elif sort_param == "author":
        products = products.order_by("author")
    elif sort_param == "price":
        products = products.order_by("discount_price")
    elif sort_param == "publication_date":
        products = products.order_by("-created_at")

    products_filter = ProductFilter(request.GET, queryset=products)
    product_filter_form = products_filter.form
    products_filter_queryset = products_filter.qs

    products_per_page = 8
    paginator = Paginator(products_filter_queryset, products_per_page)
    page_number = request.GET.get("page")
    products_on_page = paginator.get_page(page_number)

    context = {
        "category": category,
        "products": products_on_page,
        "sort_param": sort_param,
        "filter_form": product_filter_form,
    }
    return render(request, "App/products/category_list.html", context)


def search_products(request):
    if request.method == "POST":
        query = request.POST["search"]

        products = Product.objects.filter(
            Q(title__icontains=query)
            | Q(product_type__name__icontains=query)
            | Q(category__name__icontains=query)
        )

        return render(
            request, "App/index.html", context={"query": query, "products": products}
        )

    return render(request, "App/index.html")


def delete_review(request, id):
    review = get_object_or_404(ProductReview, pk=id)
    review.delete()
    messages.success(request, "Review deleted")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def like_comment(request):
    if request.POST.get("action") == "post":
        review_id = request.POST.get("review_id")

        try:
            comment = ProductReview.objects.get(id=review_id)
            comment.like_count += 1
            comment.save()

            # Return the updated like count as JSON
            return JsonResponse({"like_count": comment.like_count})
        except ProductReview.DoesNotExist:
            # Handle the case where the comment doesn't exist
            return JsonResponse({"error": "Comment not found"}, status=404)

    # Handle other request methods or non-AJAX requests
    return JsonResponse({"error": "Invalid request"}, status=400)


def export_data(request):
    product_model_resource = ProductModelResource()
    dataset = product_model_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_model_data.csv"'
    return response
