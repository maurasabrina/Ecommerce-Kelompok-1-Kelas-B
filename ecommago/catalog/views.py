from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Page, Product, Category, Cart, CartItem, Order, Review

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'categories': categories, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'catalog/cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price(),
    )
    cart.items.all().delete()  # Kosongkan keranjang setelah checkout
    return render(request, 'catalog/order_confirmation.html', {'order': order})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
    return redirect('product_detail', slug=product.slug)

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'catalog/page_detail.html', {'page': page})
