# CRIANDO MODELS
Começaremos agora a interagir com o banco de dados e, para isso, usaremos os **models** do Django. 

Vamos abrir o arquivo **<nome_do_app>/models.py**. Nele vamos definir as classes que serão criadas no banco de dados. Para este projeto, vou criar duas classes. A primeira será **Produto** e a segunda será **Categoria**. Esta última será associada a uma Produto já existente. O arquivo **models.py** ficará assim:

**models.py**
```py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    categories = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
```
Você criou duas classes em Django, **Category** e **Product**, usando o **models**, que facilita nosso trabalho. Não precisamos definir IDs, o Django cuida disso.

Usei tipos de dados como Char, Integer, e DecimalField para representar texto, inteiro e decimal. Há muitos outros tipos, veja [aqui](https://docs.djangoproject.com/en/4.2/ref/models/fields/).

O ``ForeignKey`` no **Product** indica que ele está associado a uma **Category**. ``on_delete=models.PROTECT`` significa que uma Category não pode ser excluída se um Product estiver associado.

Outras opções comuns para `on_delete` são ``CASCADE`` (excluiria também o Product), ``SET_ NULL`` (o campo Category do Product se tornaria nulo) e ``DO_NOTHING`` (o campo Category do Product permaneceria inalterado).

O `def__str__` personaliza como nossas classes são impressas. Nesse caso, apenas os nomes são exibidos.

Para adicionar essas classes ao banco, use os comandos no terminal:
```bash
python manage.py makemigrations
python manage.py migrate
```
---
Por fim, vamos fazer as classes aparecerem na página admin. Isso vai nos permitir interagir com elas imediatamente. Para isso, vamos abrir o arquivo **admin.py** e adicionar:

**admin.py**
```py
from django.contrib import admin
from .models import Category, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
```
Com isso, devemos conseguir acessar o link admin e ver nossas classes. Aproveite de cadastre objetos no sistema.
	
- [localhost:8000/admin](http://127.0.0.1:8000/admin)

Pelo link admin, já conseguimos realizar o CRUD completo. Porém, não é recomendado usar o admin padrão do Django, então criaremos nosso próprio CRUD no frontend do projeto.

---