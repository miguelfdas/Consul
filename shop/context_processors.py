from .models import Category
from .cart import Cart

def categories(request):
    return {'categories': Category.objects.all()}

def shop_context(request):
    return {
        'categories': Category.objects.all(),
        'cart': Cart(request)
    }