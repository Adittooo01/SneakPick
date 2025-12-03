

# cart/views.py
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

@login_required(login_url='users:login')
def add_to_cart(request):
    """
    Add a product to the authenticated user's cart.
    - If the item exists, increase its quantity.
    - If not, create it with the provided quantity (default 1).
    Then redirect to the cart page.
    """
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        # Use the authenticated user directly
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart:render_cart')

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

@login_required(login_url='users:login')
def render_cart(request):
    """
    Build a structured cart payload the template expects:
    cart.items: [{id, product_name, price, quantity, total_price, product_id}, ...]
    cart.total: number
    """
    # Use the authenticated user directly
    cart, _ = Cart.objects.get_or_create(user=request.user)

    items = []
    for item in cart.items.select_related('product'):
        items.append({
            'id': item.id,
            'product_name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'total_price': item.total_price,
            'product_id': item.product.id,
        })

    context = {
        'cart': {
            'items': items,
            'total': cart.total,
        }
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='users:login')
def update_cart(request):
    if request.method == "POST":
        cart_item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif action == "remove":
            cart_item.delete()
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)
def cart(request):
    """
    Legacy view: redirect to the canonical cart rendering view.
    """
    return redirect('cart:render_cart')