from django import forms

from orders.models import OrderReturn


class OrderReturnForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea)
    screenshot = forms.FileField(
        label="Upload files",
        widget=forms.FileInput(
            attrs={"name": "screenshot", "accept": "image/*", "id": "screenshot"}
        ),
    )

    class Meta:
        model = OrderReturn
        fields = ["screenshot", "reason"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["screenshot"].required = False
