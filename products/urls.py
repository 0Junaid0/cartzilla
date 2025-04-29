from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/add/', views.product_add_view, name='add_product'),
    path('product/edit/<int:pk>/', views.product_edit_view, name='edit_product'),
    path('product/delete/<int:pk>/', views.product_delete_view, name='delete_product'),
    path('product/bargain/<int:pk>/', views.bargain_offer_view, name='bargain_offer'),
    path('products/', views.products_view, name='products'),
    path('seller/dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
]
