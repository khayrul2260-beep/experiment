from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()

class CustomerRegistrationForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Enter your email",
            }
        )
    )

    phone = forms.CharField(
        label="Phone Number",
        max_length=11,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "inputmode": "numeric",
                "placeholder": "01XXXXXXXXX (Optional)",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
        min_length=8,
        max_length=128,
        required=True
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
        min_length=8,
        max_length=128,
        required=True
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
            "password",
            "confirm_password",
        ]

    def clean_email(self):

        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_phone(self):

        phone = self.cleaned_data.get("phone", "").strip()

        # Phone is optional
        if not phone:
            return ""

        if not phone.isdigit():
            raise forms.ValidationError(
                "Invalid phone number. Phone number must contain only numbers."
            )

        if len(phone) != 11:
            raise forms.ValidationError(
                "Invalid phone number. Phone number must be exactly 11 digits."
            )

        if not phone.startswith("01"):
            raise forms.ValidationError(
                "Invalid phone number. Phone number must start with 01."
            )

        # No uniqueness check:
        # the same phone number may be used by multiple accounts.
        return phone

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if (
            password
            and confirm_password
            and password != confirm_password
        ):
            self.add_error(
                "confirm_password",
                "Passwords do not match."
            )

        return cleaned_data

class CustomerLoginForm(forms.Form):

    email = forms.EmailField(
        label="Email Address",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        )
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()



class CustomerProfileForm(forms.ModelForm):

    full_name = forms.CharField(
        label="Full Name",
        max_length=150,
        required=True
    )

    phone = forms.CharField(
        label="Phone Number",
        max_length=11,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "inputmode": "numeric",
                "placeholder": "01XXXXXXXXX (Optional)",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["full_name"].initial = (
            f"{self.instance.first_name} "
            f"{self.instance.last_name}"
        ).strip()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            return ""

        if (
            not phone.isdigit()
            or len(phone) != 11
            or not phone.startswith("01")
        ):
            raise forms.ValidationError(
                "Enter a valid 11-digit Bangladeshi phone number."
            )

        return phone

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = self.cleaned_data["full_name"].strip()
        name_parts = full_name.split(maxsplit=1)

        user.first_name = name_parts[0]
        user.last_name = (
            name_parts[1] if len(name_parts) > 1 else ""
        )

        if commit:
            user.save()

        return user


class CustomerPasswordChangeForm(PasswordChangeForm):

    new_password1 = forms.CharField(
        label="New Password",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
            }
        )
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password",
            }
        )
    )

    def clean_new_password1(self):

        password = self.cleaned_data.get("new_password1")

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long."
            )

        if len(password) > 128:
            raise forms.ValidationError(
                "Password cannot exceed 128 characters."
            )

        return password

