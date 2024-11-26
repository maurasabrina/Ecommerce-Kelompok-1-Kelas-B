from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.utils.safestring import mark_safe


class LoginForm(forms.Form):
    username = forms.CharField(
        label=mark_safe('Username <span class="text-danger">*</span>'),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukan Username"
            }
        )
    )
    password = forms.CharField(
        label=mark_safe('Password <span class="text-danger">*</span>'),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Masukan Password Minimal 8 karakter"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name"
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name"
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Minimal 8 karakter"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Konfirmasi Password"
            }
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "+62813xxx"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "namaemail@gmail.com"
            }
        )
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Tanggal Lahir (YYYY-MM-DD)"
            }
        ),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'birth_date', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        user.birth_date = self.cleaned_data.get("birth_date")
        user.is_pelanggan = True
        if commit:
            user.save()
        return user


    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email has been registered...")
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Password Baru",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Baru'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Konfirmasi Password Baru",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Password Baru'}),
        strip=False,
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 6:
            raise forms.ValidationError("Password harus terdiri dari minimal 6 karakter.")
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password tidak sesuai.")
        return password2

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        label='Email'
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama Anda'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama Anda'}),
            'email': forms.TextInput(attrs={'placeholder': 'Masukkan email Anda'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Masukkan nomor telepon Anda'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Tambahkan validasi email di sini jika diperlukan
        return email

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class PasswordResetConfirmForm(forms.Form):
    verification_code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
