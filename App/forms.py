from django import forms

from .models import ProductImage, ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["review_text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["review_text"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Your comment"}
        )
