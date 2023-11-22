from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail

from .models import Address, Customer


class MyCustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        send_mail(
            "Subject here",
            "Here is the message.",
            "mohshibilicv@gmail.com",
            ["project.nasra@gmail.com"],
            fail_silently=False,
        )

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "mb-2", "placeholder": "Your email", "id": "login-username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "mb-2",
                "placeholder": "Your password",
                "id": "login-password",
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, email=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        error_messages={"required": "The Email is required"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = (
            "username",
            "email",
        )

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        user = Customer.objects.filter(username=username)

        if user.count():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_password2(self):
        pass1 = self.cleaned_data["password"]
        pass2 = self.cleaned_data["password2"]

        if pass1 != pass2:
            raise forms.ValidationError("Passwords didn't match")

        if len(pass1) < 8:
            raise forms.ValidationError("Password must have 8 characters")

        return pass1

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("The email is already taken")

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "mb-2", "placeholder": "Enter your username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "mb-2", "placeholder": "Enter your email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "mb-2", "placeholder": "Enter the password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "mb-2", "placeholder": "Confirm your password"}
        )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account Email",
        max_length=155,
        widget=forms.TextInput(
            attrs={
                "class": "mb-2",
                "placeholder": "email",
                "id": "form-email",
                "readonly": False,
            }
        ),
    )
    mobile = forms.CharField(
        label="Mobile Number",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "mb-2",
                "placeholder": "Mobile Number",
                "id": "form-firstname",
            }
        ),
    )
    profile = forms.FileField(
        label="Profile",
        widget=forms.FileInput(
            attrs={"name": "profile", "accept": "image/*", "id": "imageInput"}
        ),
    )

    class Meta:
        model = Customer
        fields = ("profile", "email", "username", "mobile")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")

        if len(mobile) < 10:
            raise forms.ValidationError("Please enter a valid mobile number.")

        return mobile


class PasswordChangeCustomForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "email",
            "phone",
            "address_line",
            "address_line2",
            "town_city",
            "postcode",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Email"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Phone Number"}
        )
        self.fields["address_line"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Address Line 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Address Line 2"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Town/ City"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "mb-2 account-form", "placeholder": "Postcode"}
        )
