"""ClothingStoreDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ClothingStoreApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # админ панель
    path('admin/', admin.site.urls),

    # главная страница
    path('', views.index, name="index"),
    path('index/', views.index, name="index1"),

    # каталог для пользователя
    path('catalog/', views.catalog, name="catalog"),

    # каталог для админа 
    path('products-administration/', views.products_administration, name="products-administration"),
    path('add-to-db/', views.add_to_db, name="add-to-db"),
    path('delete-from-db-<int:item>/', views.delete_from_db, name="delete-from-db"),
    path('edit-in-db-<int:item>/', views.edit_in_db, name="edit-in-db"),

    # страница товара
    path('single-product-<int:item>/', views.single_product, name="single-product"),

    # корзина
    path('cart/', views.cart, name="cart"),
    path('add-to-cart-<int:item>/', views.add_to_cart, name="add-to-cart"),
    path('delete-from-cart-<int:item>/', views.delete_from_cart, name='delete-from-cart')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)