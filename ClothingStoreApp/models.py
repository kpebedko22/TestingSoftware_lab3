from django.db import models
from django.urls import reverse

# Модели БД магазина одежды

class Size(models.Model):
    PK_Size = models.AutoField(db_column='PK_Size', primary_key=True) 
    sizeName = models.CharField(db_column='sizeName', max_length=100, verbose_name='Наименование')

    class Meta:
        db_table = 'Size'
        verbose_name_plural = 'Размеры одежды'
        verbose_name = 'Размер одежды'

    def __str__(self):
        return self.sizeName

class Category(models.Model):
    PK_Category = models.AutoField(db_column='PK_Category', primary_key=True) 
    categoryName = models.CharField(db_column='categoryName', max_length=100, verbose_name='Наименование')

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.categoryName

class Color(models.Model):
    PK_Color = models.AutoField(db_column='PK_Color', primary_key=True) 
    colorName = models.CharField(db_column='colorName', max_length=100, verbose_name='Наименование')

    class Meta:
        db_table = 'Color'
        verbose_name_plural = 'Цвета'
        verbose_name = 'Цвет'

    def __str__(self):
        return self.colorName

class Clothes(models.Model):
    PK_Clothes = models.AutoField(db_column='PK_Clothes', primary_key=True)
    clothesName = models.CharField(db_column='clothesName', max_length=100, verbose_name='Наименование')
    PK_Category = models.ForeignKey(Category, models.DO_NOTHING, db_column='PK_Category', verbose_name='Категория')
    PK_Size = models.ForeignKey(Size, models.DO_NOTHING, db_column='PK_Size', verbose_name='Размер')
    PK_Color = models.ForeignKey(Color, models.DO_NOTHING, db_column='PK_Color', verbose_name='Цвет')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена')
    imagePath = models.ImageField(db_column='imagePath', max_length=255, blank=True, null=True, verbose_name='Фото')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return 'Товар: {}; {}; {}; {}; {};'.format(self.clothesName, self.PK_Category, self.PK_Size, self.PK_Color, self.price)
    
    def get_absolute_url(self):
        return reverse('single-product',args=[str(self.PK_Clothes)])

    class Meta:
        db_table = 'Clothes'
        verbose_name_plural = 'Одежда'
        verbose_name = 'Одежда'

class Cart(models.Model):
    PK_Cart = models.AutoField(db_column='PK_Cart', primary_key=True)
    items = models.ManyToManyField(Clothes, db_column='items', verbose_name='Товары')
    totalPrice = models.DecimalField(db_column='totalPrice', max_digits=15, decimal_places=2, default=0, verbose_name='Общая сумма')
    totalItems = models.PositiveIntegerField(db_column='totalItems', default=0, verbose_name='Количество товаров')

    def UpdateTotal(self):
        self.totalPrice = sum(item.price for item in self.items.all())
        self.totalItems = len(self.items.all())
        self.save()

    def __str__(self):
        return 'Корзина: {} товар(ов), цена: {}'.format(self.totalItems, self.totalPrice)

    class Meta:
        db_table = 'Cart'
        verbose_name_plural = 'Корзины'
        verbose_name = 'Корзина'

class ClothesOrder(models.Model):
    PK_ClothesOrder = models.AutoField(db_column='PK_ClothesOrder', primary_key=True)
    nameClient = models.CharField(db_column='nameClient', max_length=255, verbose_name='Имя')
    phoneClient = models.CharField(db_column='phoneClient', max_length=100, verbose_name='Телефон')
    emailClient = models.EmailField(db_column='emailClient', max_length=254, verbose_name='E-mail')
    cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='PK_Cart', null=True, blank=True, verbose_name='Корзина')

    def __str__(self):
        return '{}; {}; {}'.format(self.nameClient, self.phoneClient, self.emailClient)

    class Meta:
        db_table = 'ClothesOrder'
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'