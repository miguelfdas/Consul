from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL friendly name")

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size_or_type = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")

    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return f"{self.product.name} - {self.size_or_type} (€{self.price})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False, help_text="Imagem principal de apresentação")

    def __str__(self):
        return f"Image for {self.product.name}"
    
class Order(models.Model):
    PAYMENT_CHOICES = (
        ('mbway', 'MB Way'),
        ('tb', 'Transferência Bancária'),
        ('entrega', 'Pagamento na Entrega'),
    )
    
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='mbway')
    
    products_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Encomenda #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity