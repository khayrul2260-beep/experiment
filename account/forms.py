from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()
class CustomerRegistrationForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=150,
        required=True
    )

    username = forms.CharField(
        label="Phone Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "inputmode": "numeric",
                "placeholder": "01XXXXXXXXX",
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
            "username",
            "password",
            "confirm_password",
        ]

    def clean_username(self):
    
        username = self.cleaned_data["username"].strip()
    
        # Only numbers
        if not username.isdigit():
            raise forms.ValidationError(
                "Invalid phone number. Phone number must contain only numbers."
            )
    
        # Exactly 11 digits
        if len(username) != 11:
            raise forms.ValidationError(
                "Invalid phone number. Phone number must be exactly 11 digits."
            )
    
        # Must start with 01
        if not username.startswith("01"):
            raise forms.ValidationError(
                "Invalid phone number. Phone number must start with 01."
            )
    
        # Unique phone number
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "An account with this phone number already exists."
            )
    
        return username

class CustomerLoginForm(forms.Form):

    username = forms.CharField(
        label="Phone Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number",
                "autocomplete": "username",
                "inputmode": "numeric",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
        required=True
    )


class CustomerProfileForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=150,
        required=True
    )

    username = forms.CharField(
        label="Phone Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "inputmode": "numeric",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "username",
            "profile_image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Existing first_name + last_name
        self.fields["full_name"].initial = (
            f"{self.instance.first_name} "
            f"{self.instance.last_name}"
        ).strip()

    def clean_username(self):

        username = self.cleaned_data["username"].strip()

        # Only numbers
        if not username.isdigit():
            raise forms.ValidationError(
                "Invalid phone number. Phone number must contain only numbers."
            )

        # Exactly 11 digits
        if len(username) != 11:
            raise forms.ValidationError(
                "Invalid phone number. Phone number must be exactly 11 digits."
            )

        # Must start with 01
        if not username.startswith("01"):
            raise forms.ValidationError(
                "Invalid phone number. Phone number must start with 01."
            )

        # Check duplicate username
        if User.objects.filter(
            username=username
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "This phone number is already in use."
            )

        return username

    def clean_email(self):

        email = self.cleaned_data["email"].strip().lower()

        return email

    def save(self, commit=True):

        user = super().save(commit=False)

        full_name = self.cleaned_data["full_name"].strip()

        # Full name → first_name + last_name
        name_parts = full_name.split(maxsplit=1)

        user.first_name = name_parts[0]

        if len(name_parts) > 1:
            user.last_name = name_parts[1]
        else:
            user.last_name = ""

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

