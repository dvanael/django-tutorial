# Criando Models
Começaremos agora a interagir com o banco de dados e, para isso, usaremos os **models** do Django. 

Vamos abrir o arquivo **<nome_do_app>/models.py**. Nele vamos definir as classes que serão criadas no banco de dados. Para este projeto, vou criar duas classes. A primeira será **Produto** e a segunda será **Categoria**. Esta última será associada a uma Produto já existente. O arquivo **models.py** ficará assim:
### models.py
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

Ao criar uma classe, usamos o models do Django como base para que ele lide com algumas coisas para nós, facilitando o nosso trabalho. Se olhar atentamente, verá que não precisei definir o ID (ou PrimaryKey, PK) para nenhuma das duas classes, pois o Django já irá lidar com isso para nós.

Outra coisa importante são os tipos de dados. Eu utilizei Char, Integer e DecimalField, que representam texto, inteiro e decimal, mas existem dezenas de outros tipos. Para mais informações desses tipos e dos outros, você pode acessar o [link oficial do Django](https://docs.djangoproject.com/en/4.2/ref/models/fields/).
	
Ou acessar essa [versão em português](https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django/Models).

Também utilizei *'ForeignKey'* no objeto Produto. A tradução seria Chave Estrangeira e indica que é um dado que vem de outra classe (nesse caso, a classe Produto usando algo da classe Categoria).

Ainda no ForeignKey, mesma linha, há o *'on_delete=models.PROTECT'*. Como o Produto está sendo associada a uma Categoria, esse 'on_delete' indica o que irá acontecer com uma Categoria caso o Produto a qual ela está associada seja deletada. Utilizando PROTECT, a Categoria não pode ser deletada até que nenhuma Produto esteja associada a ela.

Outras opções comuns são CASCADE, onde a Produto também seria deletada; SET_NULL, onde o campo Categoria do Produto seria substituído por NULL (Nulo); e o DO_NOTHING, onde o campo Categoria do Produto seria substituído por "vazio" ().

Por fim, temos o **def __str__**. Em breve, veremos que podemos pedir para que o Django imprima uma classe do banco para nós, mas, por padrão, ele iria imprimir algo como:
- object (1)
- object (2)

Por isso, definimos a função e damos uma formatação que nos seja mais interessante. Da forma que foi definido, apenas serão impresso os nomes dos objetos.

Após as classes serem definidas, precisamos adicioná-las ao banco. Para isso, vamos digitar no terminal os seguintes comandos:
```
python manage.py makemigrations
python manage.py migrate
```

Por fim, vamos fazer as classes aparecerem na página admin. Isso vai nos permitir interagir com elas imediatamente. Para isso, vamos abrir o arquivo **admin.py** e adicionar:
### admin.py
```py
from django.contrib import admin
from .models import Category, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
```
Com isso, devemos conseguir acessar o link admin e ver nossas classes.
	http://127.0.0.1:8000/admin

Pelo link admin, já conseguimos realizar o CRUD completo. Porém, não é recomendado usar o admin padrão do Django, então criaremos nosso próprio CRUD no frontend do projeto.