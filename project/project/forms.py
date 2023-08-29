from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class SignupForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width:100%;"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "vTextField", "style": "width:100%; padding:8px;"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "vTextField", "style": "width:100%;"}
        )
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "vTextField", "style": "width:100%; padding:8px;"}
        ),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # Validate the password against Django's password validation rules
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords don't match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Ensure you want every user to be a staff member
        user.is_staff = True
        if commit:
            user.save()
        return user


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "vTextField form-row", "style": "width:100%; padding:8px;"}
        ),
    )

    def save(self, *args, **kwargs):
        # Your custom logic here
        # ...

        # Ensure the default behavior still occurs
        super().save(*args, **kwargs)


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "vTextField", "style": "width:100%;"}
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "vTextField", "style": "width:100%;"}
        )
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
