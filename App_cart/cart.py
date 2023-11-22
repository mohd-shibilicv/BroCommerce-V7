from decimal import Decimal

from django.conf import settings

from App.models import Product
from checkout.models import Coupon, DeliveryOptions


class Cart:
    """
    Class Representing user's shopping cart
    """
    def __init__(self, request):
        """
        Initial cart configurations
        """
        self.session = request.session
        cart = self.session.get(settings.BASKET_SESSION_ID)

        if settings.BASKET_SESSION_ID not in request.session:
            cart = self.session[settings.BASKET_SESSION_ID] = {}

        self.cart = cart
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product, productquantity):
        """
        Adding and Updating users cart session data
        """

        if productquantity > product.product_stock:
            return 0
    
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] = productquantity
        else:
            if product.discount_price:
                self.cart[product_id] = {
                    "price": str(product.discount_price),
                    "quantity": int(productquantity),
                    "stock": int(product.product_stock),
                }
            else:
                self.cart[product_id] = {
                    "price": str(product.regular_price),
                    "quantity": int(productquantity),
                    "stock": int(product.product_stock),
                }

        self.save()

    def get_productquantity(self, product, productquantity):
        """
        Return cart item quantity
        """
        if product in self.cart:
            return float(productquantity)

    def __iter__(self):
        """
        Collect the session_id in the session data to query the database
        and return products
        """
        products = Product.objects.filter(id__in=self.cart.keys())
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for product_id, item in list(cart.items()):
            if item['quantity'] > item['stock']:
                # Quantity exceeds stock, remove the item from the cart
                del self.cart[product_id]
                continue

            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Get the cart data and count the quantity of items
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal_price(self):
        """
        Get the total amount of a product
        """
        if self.__len__() != 0:
            return sum(
                Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
            )
        return Decimal(0)

    @property
    def coupon(self):
        """
        Get the user's coupon
        """
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """
        Get the coupon discount
        """
        if self.coupon:
            return (self.coupon.discount / Decimal("100")) * self.get_subtotal_price()
        return Decimal("0")

    def get_subtotal_price_after_discount(self):
        """
        Get the price after applying the discount
        """
        if self.__len__() != 0:
            return self.get_subtotal_price() - self.get_discount()
        return Decimal(0)

    def get_total_price(self):
        """
        Get the total amount of a product
        """
        new_price = 0.00
        if self.coupon:
            subtotal = self.get_subtotal_price_after_discount()
        else:
            subtotal = self.get_subtotal_price()

        if "purchase" in self.session:
            new_price = DeliveryOptions.objects.get(
                id=self.session["purchase"]["delivery_id"]
            ).delivery_price

        total = subtotal + Decimal(new_price)
        if self.__len__() != 0:
            return total
        return Decimal(0)

    def get_total_price_with_tax(self):
        """
        Get the total amount of a product
        """
        new_price = 0.00
        tax_price = 2.99
        if self.coupon:
            subtotal = self.get_subtotal_price_after_discount()
        else:
            subtotal = self.get_subtotal_price()

        if "purchase" in self.session:
            new_price = DeliveryOptions.objects.get(
                id=self.session["purchase"]["delivery_id"]
            ).delivery_price
            new_price = Decimal(new_price) + Decimal(tax_price)

        total = subtotal + Decimal(new_price)

        if self.__len__() != 0:
            return Decimal(round(total, 2))
        return Decimal(0)

    def get_delivery_price(self):
        """
        Get the delivery price
        """
        new_price = 0.00

        if self.__len__() != 0:
            if "purchase" in self.session:
                new_price = DeliveryOptions.objects.get(
                    id=self.session["purchase"]["delivery_id"]
                ).delivery_price
        else:
            return Decimal(0)

        return new_price

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def update(self, product, quantity):
        """
        Update product quantity in session data
        """
        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity

        self.save()

    def cart_update_delivery(self, delivery_price=0):
        """
        Update Delivery Option and it's price
        """
        if self.coupon:
            subtotal = self.get_subtotal_price_after_discount()
        else:
            subtotal = self.get_subtotal_price()

        total = subtotal + Decimal(delivery_price)
        return total

    def save(self):
        """
        Save Session Changes
        """
        self.session.modified = True

    def clear(self):
        """
        Clear the session
        """
        del self.session[settings.BASKET_SESSION_ID]
        if self.session["address"]:
            del self.session["address"]
        if self.session["purchase"]:
            del self.session["purchase"]
        self.save()
