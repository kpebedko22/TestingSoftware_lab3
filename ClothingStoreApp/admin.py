from django.contrib import admin
from .models import Size, Category, Color, Clothes, ClothesOrder, Cart

# Register your models here.
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Clothes)
admin.site.register(Cart)
admin.site.register(ClothesOrder)
