from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username","email","password1","password2")

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=80)
    state = forms.CharField(max_length=80)
    pincode = forms.CharField(max_length=10)
    payment_method = forms.ChoiceField(choices=[
        ("COD","Cash on Delivery"),("UPI","UPI"),("CARD","Credit / Debit Card"),
        ("NETBANKING","Net Banking")
    ])

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating","comment")
        widgets = {"rating": forms.Select(choices=[(i,i) for i in range(1,6)])}
