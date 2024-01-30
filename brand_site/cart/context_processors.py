from .cart import Cart


def cart(request):
    return {'cart': Cart(request),
            'total_len': Cart(request).get_all_items()}