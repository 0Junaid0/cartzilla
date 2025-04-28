from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, ProductReview, BargainOffer
from .forms import ProductForm, ReviewForm, BargainOfferForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/home.html', {'products': products, 'categories': categories})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted!')
            return redirect('product_detail', pk=product.pk)
    else:
        review_form = ReviewForm()

    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews, 'review_form': review_form})

@login_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product added!')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated!')
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('seller_dashboard')

@login_required
def bargain_offer_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = BargainOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.product = product
            offer.buyer = request.user
            offer.save()
            messages.success(request, 'Bargain offer sent!')
            return redirect('product_detail', pk=pk)
    else:
        form = BargainOfferForm()
    return render(request, 'products/bargain_form.html', {'form': form})
