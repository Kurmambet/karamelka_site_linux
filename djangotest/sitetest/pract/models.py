from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# def translit_to_eng(s: str) -> str:
#     d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
#          'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
#          'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
#          'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
#          'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
#
#     return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class StockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_stock=Goods.Status.InStock)

class Goods(models.Model):

    class Status(models.IntegerChoices):
        OutOfStock = 0, 'Нет в наличии'
        InStock = 1, 'Есть в наличии'

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Ссылка',
                            validators=[
                            MinLengthValidator(5, message='Минимум 5 символов'),
                            MaxLengthValidator(100, message='Максимум 100 символов'),
                           ])
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True,
                              null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создание')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Врем обновления')
    is_stock = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                default=Status.InStock, verbose_name='Наличие')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products_by_cat', verbose_name='Категория')
    sup = models.ForeignKey('Supplier', on_delete=models.PROTECT, related_name='products_by_sup', verbose_name='Поставщик')

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='products_changes', null=True, default=None, verbose_name='Редактировал')

    objects = models.Manager()
    stocked = StockManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вся продукция'
        verbose_name_plural = 'Вся продукция'
        ordering = ['time_create']
        indexes = [
            models.Index(fields=['time_create'])
        ]

    def get_absolute_url(self):
        return reverse('tovar', kwargs={'tovar_slug': self.slug} )

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)






class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Ссылка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукция по категориям'
        verbose_name_plural = 'продукция по категориям'



class Supplier(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Поставщик')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Ссылка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукция по поставщикам'
        verbose_name_plural = 'продукция по поставщикам'



class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')





# class CommentsTovar(models.Model):
#     slug = models.SlugField(max_length=255, unique=True, db_index=True,)


