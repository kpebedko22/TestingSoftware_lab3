from django import forms
from .models import Clothes, Size, Color, Category, ClothesOrder, Cart


class ClothesForm(forms.ModelForm):

    clothesName = forms.CharField(max_length=100, required=True, label='')
    clothesName.widget.attrs.update({
        'class' : 'form-control btn-outline-none', 
        'placeholder': 'Наименование'
        }) 

    PK_Category = forms.ModelChoiceField(queryset = Category.objects.all(), label='', required=True, empty_label='Категория')
    PK_Category.widget.attrs.update({'class' : 'form-control btn-outline-none'}) 

    PK_Size = forms.ModelChoiceField(queryset = Size.objects.all(), label='', required=True, empty_label='Размер')
    PK_Size.widget.attrs.update({'class' : 'form-control btn-outline-none'}) 

    PK_Color = forms.ModelChoiceField(queryset = Color.objects.all(), label='', required=True, empty_label='Цвет')
    PK_Color.widget.attrs.update({'class' : 'form-control btn-outline-none'}) 

    price = forms.DecimalField(decimal_places = 2, label='', required=True)
    price.widget.attrs.update({
        'class' : 'form-control btn-outline-none',
        'placeholder': 'Цена',
        'min':'0'
        })

    imagePath = forms.ImageField(label='Фото:', required=False)
    imagePath.widget.attrs.update({'class' : 'form-control btn-outline-none'})

    description = forms.CharField(label='', widget=forms.Textarea, required=True)
    description.widget.attrs.update({
        'class' : 'form-control btn-outline-none',
        'placeholder': 'Описание'
        }) 

    class Meta:
        model = Clothes
        fields = ['PK_Clothes', 'clothesName', 'PK_Category', 'PK_Size', 'PK_Color', 'price', 'imagePath', 'description']

class ClothesOrderForm(forms.ModelForm):
    nameClient = forms.CharField(max_length=255, required=True, label='')
    nameClient.widget.attrs.update({
        'class' : 'form-control btn-outline-none', 
        'placeholder': 'Имя'
        }) 

    phoneClient = forms.CharField(max_length=100, required=True, label='')
    phoneClient.widget.attrs.update({
        'class' : 'form-control btn-outline-none', 
        'placeholder': 'Телефон'
        }) 

    emailClient = forms.EmailField(max_length=254, required=True, label='')
    emailClient.widget.attrs.update({
        'class' : 'form-control btn-outline-none', 
        'placeholder': 'E-mail'
        }) 

    cart = forms.ModelChoiceField(queryset = Cart.objects.all(), label='', required=False)
    cart.widget.attrs.update({'hidden' : 'true'})

    class Meta:
        model = ClothesOrder
        fields = ['PK_ClothesOrder', 'nameClient', 'phoneClient', 'emailClient', 'cart']
