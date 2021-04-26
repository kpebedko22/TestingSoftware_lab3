from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Clothes, ClothesOrder, Cart
from .forms import ClothesForm, ClothesOrderForm

def index(request):
    return render(request, 'index.html', {'cart': Cart.objects.all().last() })

def catalog(request):
    clothes = Clothes.objects.all()
    return render(request, 'catalog.html', {"clothes": clothes,'cart': Cart.objects.all().last()})

def products_administration(request):
    clothes = Clothes.objects.all()
    return render(request, 'products-administration.html', {"clothes": clothes,'cart': Cart.objects.all().last()})

def single_product(request, item):
    currentItem = Clothes.objects.get(PK_Clothes=item)
    return render(request, 'single-product.html', {"singleItem": currentItem,'cart': Cart.objects.all().last()})

def add_to_db(request):
    # добавление товара в бд

    if request.method == 'POST':
        # создание формы с заполненными полями
        form = ClothesForm(request.POST, request.FILES)
        
        if form.is_valid():
            # запись в базу
            form.save()

            # переход к странице администрирования
            return HttpResponseRedirect('/products-administration')

    # создание пустой формы
    form = ClothesForm()
    return render(request, "product-editing.html", {'form': form,'cart': Cart.objects.all().last()})

def delete_from_db(request, item):
    # удаление товара из бд

    currentItem = Clothes.objects.get(PK_Clothes=item)
    currentItem.delete()
    return HttpResponseRedirect('/products-administration')

def edit_in_db(request, item):
    # редактирование товара в бд
    
    currentItem = Clothes.objects.get(PK_Clothes=item)

    if request.method == 'POST':
        # создание формы с заполненными полями
        form = ClothesForm(request.POST, request.FILES)

        if form.is_valid():

            # изменение полей
            currentItem.clothesName = form.cleaned_data["clothesName"]
            currentItem.PK_Category = form.cleaned_data["PK_Category"]
            currentItem.PK_Size = form.cleaned_data["PK_Size"]
            currentItem.PK_Color = form.cleaned_data["PK_Color"]
            currentItem.price = form.cleaned_data["price"]
            currentItem.imagePath = form.cleaned_data["imagePath"]
            currentItem.description = form.cleaned_data["description"]

            # запись модели
            currentItem.save()
            return HttpResponseRedirect('/products-administration')

    # создание формы с заполнением полей данными модели
    form = ClothesForm(instance=currentItem)
    return render(request, "product-editing.html", {'form': form, 'PK': currentItem.PK_Clothes,'cart': Cart.objects.all().last()})

def cart(request):
    # страница оформления заказа

    cart = Cart.objects.all().last()
    if request.method == 'POST':
        # создание формы с заполненными полями
        form = ClothesOrderForm(request.POST)
        if form.is_valid():
            
            # проверяем что в корзине есть товары
            # чтобы не добавлять заказы с пустой корзиной в бд
            if cart.totalItems:
                # добавляем в объект заказа текущую корзину и сохраняем
                newOrder = form.save(commit=False)
                newOrder.cart = cart
                newOrder.save()

                # создаем новую корзину для товаров
                newCart = Cart()
                newCart.save()

            # обновляем страницу заказа
            return HttpResponseRedirect('/cart')

    # создание пустой формы
    form = ClothesOrderForm()
    return render(request, 'cart.html', {'cart': cart ,'form': form})

def add_to_cart(request, item):
    # добавление товара в корзину

    currentItem = Clothes.objects.get(PK_Clothes=item)

    # если корзины для товаров нет, то создаем новую
    # иначе берем последнюю 
    # (предполагается что заказа с этой корзиной не было)
    if not Cart.objects.all():
        currentCart = Cart()
        currentCart.save()
    else:
        currentCart = Cart.objects.all().last()

    currentCart.items.add(currentItem)
    currentCart.UpdateTotal()

    return HttpResponseRedirect('/cart')

def delete_from_cart(request, item):
    # удаление товара из корзины

    currentCart = Cart.objects.all().last()
    currentCart.items.remove(item)
    currentCart.UpdateTotal()
    return HttpResponseRedirect('/cart')
