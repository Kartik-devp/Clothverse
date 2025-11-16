from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.get_total_items()
            })
        
        messages.success(request, f'{product.name} added to cart.')
        return redirect('cart_detail')
    return redirect('product_list')

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_items(),
            'cart_total': cart.get_total_price(),
            'removed': True,
            'item_id': item_id,
        })

    messages.success(request, 'Item removed from cart.')
    return redirect('cart_detail')

def cart_detail(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    total_price = cart.get_total_price()
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart': cart
    })

def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    total_price = cart.get_total_price()

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        address2 = request.POST.get('address2', '').strip()
        country = request.POST.get('country', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip', '').strip()

        if not first_name or not last_name or not address or not country or not state or not zip_code:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'cart': cart
            })

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=None if request.user.is_authenticated else request.session.session_key,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            address=address,
            address2=address2,
            country=country,
            state=state,
            zip_code=zip_code,
            total=total_price,
            status='new'
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.items.all().delete()

        return redirect('checkout_success', order_id=order.id)

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart': cart
    })

def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/checkout_success.html', {
        'order': order,
    })

def update_cart_item(request, item_id):
    if request.method != 'POST':
        return redirect('cart_detail')

    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    try:
        data = request.body.decode('utf-8')
    except Exception:
        data = ''

    action = None
    if data:
        import json
        try:
            payload = json.loads(data)
            action = payload.get('action')
        except Exception:
            action = None

    removed = False
    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            removed = True
    elif action == 'set':
        # Optional: support direct set
        try:
            qty = int(payload.get('quantity', cart_item.quantity))
            if qty <= 0:
                cart_item.delete()
                removed = True
            else:
                cart_item.quantity = qty
                cart_item.save()
        except Exception:
            pass

    cart_count = cart.get_total_items()
    cart_total = cart.get_total_price()
    item_total = 0
    qty = 0
    if not removed:
        cart_item.refresh_from_db()
        qty = cart_item.quantity
        item_total = cart_item.get_total_price()

    return JsonResponse({
        'success': True,
        'removed': removed,
        'quantity': qty,
        'item_total': item_total,
        'cart_total': cart_total,
        'cart_count': cart_count,
        'item_id': item_id,
    })
