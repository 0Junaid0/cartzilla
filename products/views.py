from django.shortcuts import render, get_object_or_404, redirect

from shopping.models import Order,OrderItem
from user.models import User
from .models import Product, Category, ProductReview, BargainOffer
from .forms import ProductForm, ReviewForm, BargainOfferForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def home_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/home.html', {'products': products, 'categories': categories})

def product_detail_view(request, pk):
    user: User = request.user
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    bargain = None
    if (not user.is_anonymous) and user.is_customer():
        bargain = product.bargainoffer_set.filter(buyer=user, is_accepted=True).order_by("-accepted_at").first()

    can_review = False
    already_reviewed = False

    if request.user.is_authenticated:
        cpmpleted_order = Order.objects.filter(user=request.user , status = 'Completed')
        have_purchased = OrderItem.objects.filter(order__in = cpmpleted_order, product = product).exists()
        already_reviewed = ProductReview.objects.filter(user=request.user, product=product).exists()
        can_review = have_purchased and not already_reviewed

        if request.method == 'POST':
            if not have_purchased:
                messages.error(request , "You need to purchase the product to review it")
                return redirect('product_detail' , pk = product.pk)
            if already_reviewed:
                messages.error(request , "you have already reviewed the product")
                return redirect('product+detail', pk=product.pk)

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

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'can_review' : can_review,
        'already_reviewed' : already_reviewed,
        'bargain': bargain,
    })

def products_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/products.html', {'products': products, 'categories': categories})

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

from django.contrib.auth.decorators import login_required

@login_required
def respond_bargain_offer_view(request, offer_id, action):
    offer = get_object_or_404(BargainOffer , id=offer_id)

    if offer.product.seller != request.user:
        messages.error(request, 'You are not eligible')
        return redirect('home')

    if action == 'accept':
        offer.is_accepted = True
        offer.accepted_at = timezone.now()
        messages.success(request, 'accepted the bargain')
    elif action == 'reject':
        offer.is_accepted = False
        offer.accepted_at = None
        messages.success(request, 'rejected the bargain')

    offer.save()
    return redirect('seller_dashboard')

@login_required
def seller_dashboard_view(request):
    user: User = request.user
    if not user.is_seller():
        return redirect('home')

    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/product_dashboard.html', {'products': products})

@login_required
def delete_review_view(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)

    if review.user != request.user:
        messages.error(request, 'You cannot delete this review')
        return redirect('product_detail')

    product_id = review.product.pk
    review.delete()
    messages.success(request,'review deleted')
    return redirect('product_detail', pk=product_id)

