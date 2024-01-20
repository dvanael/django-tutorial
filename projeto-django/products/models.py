from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.CharField(max_length=255, verbose_name="Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Quantidade de Estoque")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoria")

    def __str__(self):
        return self.name