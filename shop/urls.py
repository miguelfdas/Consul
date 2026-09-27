from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    
    path('search/', views.product_search, name='product_search'),

    path('carrinho/', views.cart_detail, name='cart_detail'),
    
    path('carrinho/adicionar/', views.cart_add, name='cart_add'),
    path('carrinho/remover/<int:variant_id>/', views.cart_remove, name='cart_remove'),

    path('checkout/', views.checkout_gateway, name='checkout_gateway'),
    path('checkout/processar/', views.checkout_process, name='checkout_process'),
    path('encomenda-concluida/', views.order_success, name='order_success'),
    
    path('gestao/produtos/', views.pai_products, name='pai_products'),
    path('gestao/produtos/novo/', views.pai_product_edit, name='pai_product_add'),
    path('gestao/produtos/<int:pk>/editar/', views.pai_product_edit, name='pai_product_edit'),
    path('gestao/encomendas/', views.pai_orders, name='pai_orders'),
    path('gestao/encomendas/<int:order_id>/pagamento/', views.toggle_order_paid, name='toggle_order_paid'),

    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('perfil/', views.profile, name='profile'),
    
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]