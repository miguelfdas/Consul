from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.forms import modelform_factory, inlineformset_factory
from django.utils.text import slugify
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Category, Product, ProductVariant, Order, OrderItem
from django.contrib.auth import login
from .forms import UserRegistrationForm, CheckoutForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from decimal import Decimal
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })
    
def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    return render(request, 'shop/product_detail.html', {'product': product})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

ProductForm = modelform_factory(Product, fields=['category', 'name', 'description', 'is_active'])
VariantFormSet = inlineformset_factory(Product, ProductVariant, fields=['size_or_type', 'price', 'stock', 'sku'], extra=1, can_delete=True)

@user_passes_test(is_admin)
def pai_products(request):
    products = Product.objects.all()
    return render(request, 'shop/pai_products.html', {'products': products})

@user_passes_test(is_admin)
@transaction.atomic
def pai_product_edit(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = Product()

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = VariantFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            saved_product = form.save(commit=False)
            if not saved_product.slug:
                saved_product.slug = slugify(saved_product.name)
            saved_product.save()
            formset.instance = saved_product
            formset.save()
            return redirect('shop:pai_products')
    else:
        form = ProductForm(instance=product)
        formset = VariantFormSet(instance=product)

    return render(request, 'shop/pai_product_edit.html', {
        'form': form,
        'formset': formset,
        'product': product
    })

@user_passes_test(is_admin)
def pai_orders(request):
    orders = Order.objects.all()
    return render(request, 'shop/pai_orders.html', {'orders': orders})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('shop:pai_products')
        return reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.username == 'pai':
            messages.success(self.request, "Pai deves-me 600 euros 😂❤️")
        return response

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            # Login automático após registo
            login(request, new_user, backend='shop.backends.EmailOrUsernameModelBackend')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@require_POST
def cart_add(request):
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.add(variant=variant)
    return redirect('shop:cart_detail')

def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

def checkout_gateway(request):
    if request.user.is_authenticated:
        return redirect('shop:checkout_process')
    return render(request, 'shop/checkout_gateway.html')

def checkout_process(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'customer_name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'address': request.user.address,
            'door_number': request.user.door_number,
            'postal_code': request.user.postal_code,
            'locality': request.user.locality,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            cd = form.cleaned_data
            order.address = f"{cd['address']}, {cd['door_number']} - {cd['postal_code']} {cd['locality']}"
            
            # Cálculo de Portes
            subtotal = cart.get_total_price()
            shipping = Decimal('5.00') # Portes normais CTT
            
            if order.payment_method == 'entrega':
                shipping += Decimal('3.00') # Taxa de cobrança CTT
                
            order.products_total = subtotal
            order.shipping_cost = shipping
            order.total_price = subtotal + shipping
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order, variant=item['variant'], price=item['price'], quantity=item['quantity']
                )
            
            cart.clear()
            request.session['last_order_id'] = order.id
            return redirect('shop:order_success')
    else:
        form = CheckoutForm(initial=initial_data)

    return render(request, 'shop/checkout_process.html', {'form': form, 'cart': cart})

def order_success(request):
    order_id = request.session.get('last_order_id')
    if not order_id:
        return redirect('home')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

@user_passes_test(is_admin)
def toggle_order_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_paid = not order.is_paid
    order.save()
    return redirect('shop:pai_orders')

@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Os seus dados foram atualizados com sucesso.")
            return redirect('shop:profile')
    else:
        form = UserProfileForm(instance=request.user)
        
    user_orders = Order.objects.filter(user=request.user)
    
    return render(request, 'shop/profile.html', {
        'form': form,
        'orders': user_orders
    })
    
