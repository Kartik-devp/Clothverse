from .views import get_or_create_cart

def cart_count(request):
    if request.user.is_authenticated or request.session.session_key:
        cart = get_or_create_cart(request)
        return {'cart_count': cart.get_total_items()}
    return {'cart_count': 0}
