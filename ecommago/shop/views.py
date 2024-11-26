from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Kategori, Cart, CartItem, Order, OrderItem, Review, UserProfile



# View untuk daftar produk
def product_list(request):
    categories = Kategori.objects.all()
    products = Product.objects.filter(is_active=True)
    return render(request, 'shop/product_list.html', {'categories': categories, 'products': products})


# View untuk detail produk
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


# View untuk menambahkan produk ke keranjang
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')


# View untuk detail keranjang
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'items': items, 'total': total})


# View untuk checkout
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(user=request.user, total_amount=total)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    items.delete()  # Hapus semua item di keranjang setelah checkout
    return render(request, 'shop/order_confirmation.html', {'order': order})


# View untuk menambahkan ulasan produk
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
    return redirect('product_detail', slug=product.slug)
