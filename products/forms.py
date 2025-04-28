from django import forms
from .models import Product, ProductReview, BargainOffer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']

class BargainOfferForm(forms.ModelForm):
    class Meta:
        model = BargainOffer
        fields = ['offer_price']
