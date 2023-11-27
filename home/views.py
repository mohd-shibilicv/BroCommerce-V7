from django.shortcuts import render

from App.models import CategoryOffers, Product


def home(request):
    offer_product = Product.objects.get(slug="the-art-of-war-deluxe-edition")
    first_products = Product.objects.filter(is_active=True)[0:4]
    second_products = Product.objects.filter(is_active=True)[4:8]
    try:
        category_offer = CategoryOffers.objects.get(category=offer_product.category)
    except CategoryOffers.DoesNotExist:
        pass

    return render(
        request,
        "home/home.html",
        {
            "first_products": first_products,
            "second_products": second_products,
            "offer_product": offer_product,
            'category_offer': category_offer,
        },
    )


def about(request):
    return render(request, "home/about.html")


def blog(request):
    return render(request, "home/blog.html")


def contact(request):
    return render(request, "home/contact.html")


def error404(request):
    return render(request, "404.html")
