from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django .urls import reverse
from PIL import Image

User=get_user_model()

def get_product_url(obj, viewname):
    ct_model=obj.__class__.__name__
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug':obj.slug})


class LatestProductManager:
    @staticmethod
    def get_products_for_main_page( *args, **kwargs):
        products=[]
        ct_models=ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products=ct_model.model_class().objects.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatesProducts:

    objects=LatestProductManager()

class Category(models.Model):
    name=models.CharField(max_length=255, verbose_name='Имя категории')
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    Min_R=(400,400)
    Max_R=(800,800)

    class Meta:
        abstract=True
 
    category=models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title=models.CharField(max_length=255, verbose_name='Имя')
    slug=models.SlugField(unique=True)
    Image=models.ImageField(verbose_name='изображение')
    description=models.TextField(verbose_name='Описание', null=True)
    price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        img=Image.open(Image)
        img=self.Image
        min_height, min_width=Product.Min_R
        max_height, max_width=Product.Max_R
        if img.height<min_height or img.width<min_width:
            raise ValidationError('Разрешение изоброжение меньше минимального ')
        if img.height>max_height or img.width>max_width:
            raise ValidationError('Разрешение изоброжение больше максимального ')
        super().save(*args,**kwargs)


class Notebook(Product):

    diagonal=models.CharField(max_length=255, verbose_name='Диагональ')
    display=models.CharField(max_length=255, verbose_name='Дисплей')
    processor_freq=models.CharField(max_length=255, verbose_name='Частота процессора')
    ram=models.CharField(max_length=255, verbose_name='Операционная память ')
    video=models.CharField(max_length=255, verbose_name='Вдеокарта')
    time_without_charge=models.CharField(max_length=255, verbose_name='Время заряда батарей')

    def __str__(self):
        return "{} :{}".format(self.category.name , self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class SmartPhone(Product):
    diagonal=models.CharField(max_length=255, verbose_name='Диагональ')
    display=models.CharField(max_length=255, verbose_name='Дисплей')
    resolution=models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume=models.CharField(max_length=255, verbose_name='Обьем батарей ')
    ram=models.CharField(max_length=255, verbose_name='Операционная память ')
    sd=models.BooleanField(default=True)
    sd_volume_max=models.CharField(max_length=255, verbose_name='Максимальный объем памяти')
    main_cam_mp=models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp=models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} :{}".format(self.category.name , self.title)

    
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')
    

class Customer(models.Model):
    
    user=models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone=models.CharField(max_length=20, verbose_name='Номер телефона')
    address=models.CharField(max_length=255, verbose_name='Адрес')

    def __str__ (self):
        return "Покупатель: {} {}".format(self.user.first_name  ,self.user.last_name)

    
class CartProduct(models.Model):

    user=models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart=models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type', 'object_id')
    qty=models.PositiveIntegerField(default=1)
    total_price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} для корзины ".format(self.product.title)

class Cart(models.Model):

    owner=models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products=models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products=models.PositiveIntegerField(default=0)
    final_price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


