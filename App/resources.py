from import_export import resources

from .models import Product


class ProductModelResource(resources.ModelResource):
    class Meta:
        model = Product
