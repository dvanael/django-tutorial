# Criando um CRUD
**CRUD** é um acrônimo para **C**reate (criar), **R**ead (ler), **U**pdate (atualizar) e **D**elete (excluir). É um conjunto de operações básicas para gerenciar informações em um sistema. 

- **Create (Criar):** Adiciona novos dados ao sistema.
  
- **Read (Ler):** Recupera ou visualiza dados existentes no sistema.

- **Update (Atualizar):** Modifica ou atualiza dados já existentes no sistema.

- **Delete (Excluir):** Remove dados do sistema.

O CRUD é uma estrutura fundamental em sistemas de banco de dados e aplicativos para realizar operações básicas de manipulação de dados.

Vamos começar a criar nosso primeiro CRUD em Python no Django, grande parte do processos feitos no backend serão escritos no **viwes.py** e a parte interativa com o usuário será feita nos **templates**.

Começaremos criando nossa listagem, o READ do CRUD. Vamos criar uma pasta, **dentro de templates**, para guardar nossos HTMLs relacionados ao nosso CRUD. 
```
├── templates/
    └── products/
```
## List
Vamos programar uma função para renderizar no template todos os objetos do nosso banco de dados, assim podemos fazer nossa listagem no frontend. Lembrando de importar a classe model dos objetos que iremos utilizar.

**views.py**
```py
import .models from Products
...
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product-list.html', {'object_list': products})
```
A função **Product.objects.all()** busca todos os objetos do model que criamos anteriormente, 
utilizamos **{'object_list': products}** no render para que nossa lista de objetos seja renderizada no template.

Vamos criar o HTML **product-list.html** na nova pasta que criamos em templastes.
**product-list.html**
```html
{%extends 'base.html'%}

{%block title%}
<title>Produtos</title>
{%endblock%}

{%block content%}
<div class="content conatainer-fluid">
<div class="container">
  <div class="col-md-12 mx-auto my-3 border rounded-4 shadow">
      <div class="text-center h2 p-3 ">
          Lista de Produtos
      </div>
  </div>
  <div class="col-md-12 mx-auto my-3 border rounded-4 shadow">
    <div class="p-3">
  <!-- TOPO DA TABELA -->
      <div class="table-responsive">
      <table class="table table-striped">
        <thead class="table-secondary">
          <tr>
            <th></th>
            <th>Nome</th>
            <th>Descrição</th>
            <th>Preço (R$)</th>
            <th>Qnt. Estoque</th>
            <th>Categoria</th>
            <th>Opções</th>
          </tr>
        </thead>
        <tbody>
          {%for object in object_list%}
          <tr>
            <th><!-- reservado --></th>
            <th>{{ object.name }}</th>
            <th>{{ object.description }}</th>
            <th>{{ object.price }}</th>
            <th>{{ object.stock_quantity }}</th>
            <th>{{ object.category.name }}</th>
            <th>
          <!-- BOTÕES DE OPÇÕES -->
            </th>
          </tr>
          {%empty%}
          <tr>
            <th colspan="7">Não há produtos registrados.</th>
          </tr>
          {%endfor%}
        </tbody>
      </table>
      </div>
      
    </div>
  </div>
</div>
</div>
{%endblock%}
```
Aqui utilizamos um *for*, **{%  object in object_list %}**, para cada objeto na nossa lista de objetos, que será renderizada. Nesse *for*, usamos **{{ object.atributo }}** para cada atributo que criamos anteriormento no nosso **models.py**. 

**{% empty %}**, é uma função que é ativada quando não há objetos na nossa lista, se vazia (*if empty*).

Também, usamos classes do Bootstrap para deixar nosso template mais bonito.

Agora vamos definir a url da nossa nova função list. Adicione em urls.py:

**urls.py**
```py
from .views import *

urlpatterns = [
    ...
    path('produtos/', product_list, name='product-list'),
]
```
---
Para acessar mais facilmente, adicione um novo link na sua navbar.

**base.html**
```html
...
<li class="nav-item">
    <a class="nav-link active" href="{% url 'product-list' %}">Produtos</a></li>
...
```
---
Coloque o servidor para rodar e teste a listagem. Se você criou objetos no [**admin do Django**](http://localhost:8000/admin/), agora você poderá vê-los em [localhost:8000/produtos/](http://localhost:8000/produtos/).

## Create
Para não precisarmos entrar no admin do Django para fazer novos cadastros, criaremos um formulário em nosso frontend.

Primeiramente, é necessário criar um arquivo **forms.py** na pasta do nosso app.
```
├── products/
    └── forms.py
```
No forms.py, vamos escrever o seguinte código do nosso fórmulario, definindo qual model iremos usar e quais campos estarão nesse formúlario.

**forms.py**
```py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'category']
```
---
Utilizaremos essa classe form em nossa função create. Em views.py, vamos escrever:

**views.py**
```py
from django.shortcuts import render, redirect #importamos a função redirect do django
from .forms import ProductForm #importamos nossa classe form

...

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    context = {'form': form, 'title': 'Cadastrar Produto'}
    return render(request, 'form.html', context)
```
Nessa função, se o método de requisição for POST, definimos nosso formulário e se ele for válido, salvamos usa informações. Usamos a **função redirect** para redirecionar o usuário para a listagem assim que o formulário for salvo.

Criamos um contexto para nosso render para definir como usaremos o form e title no nosso template. Agora criaremos, na pasta template, um **form.html**.
```
├── templates/
    └── form.html
```
Esse form.html está fora da pasta products porque poderemos utlizá-lo para diferentes funções e models. Mas se preferir, pode criar um **product-form.html** na **pasta products** mas lembre defini-lo na função render.

**form.html**
```html
{%extends 'base.html'%}

{%block title%}
<title>{{title}}</title>
{%endblock%}

{%block content%}
<div class="content conatainer-fluid">
<div class="container">
  <div class="col-md-6 mx-auto my-3 border rounded-4 shadow">
    <div class="text-center h2 px-3 pt-3">
      {{title}}
    </div>
    
    <div class="p-3">
      <p class="lead">Preencha as informações necessárias.</p>
      <form method="post" action="">
        {% csrf_token %}
        {{ form.as_p }}

        <div class="text-end">
          <a class="btn btn-secondary btn-lg" href="javascript:history.back()">Voltar</a>
          <button class="btn btn-success btn-lg" type="submit">Salvar</button>
        </div>

      </form>
    </div>

  </div>
</div>  
</div>
{%endblock%}
```
Aqui, usamos o **{{ title }}** para alterar o título de acordo com a função que está sendo executada no template. 

**{% csrf_token %}** é uma medida de segurança. O mais importante, o **{{ form.as_p }}** é nosso form definido na função create é renderizado como um parágrafo na nossa página.

Agora nos resta, configurar nossa url. Também, adicionaremos um botão no topo da tabela, linkando nosso formulário.

**urls.py**
```py
path('produtos/cadastrar/', product_create, name='product-create'),
```
**product-list.html**
```html
...
<!-- TOPO DA TABELA -->
      <div class="text-end pb-3">
        <a class="btn btn-success" href="{% url 'product-create' %}">Cadastrar Produto</a>
      </div>
...
```
Rode o servidor localhost e faça o teste, adicione novos objetos a tabela.
## Update
Agora que podemos ler e adicionar novos objetos a tabela, iremos criar uma função update, para atualizar os objetos já existentes. 

Fizemos o forms.py e o form.html anteriormente, então essa etapa será mais fácil. Basta compreender a lógica.

**views.py**
```py
from django.shortcuts import render, redirect, get_object_or_404 #importamos a função get or error do Django

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    context = {'form': form, 'title': 'Atualizar Produto'}
    return render(request, 'form.html', context)
```
Por se tratar de uma atualização de um objeto, primerio buscamos o objeto em específico pela sua chave *prímária (*pk*)* juntamente da requisição, para assim, enviarmos seus dados para o formulário (*instance=product*). E seguimos o mesmo processo da função create.

Adicionamos a url para essa função.

**urls.py**
```py
path('produtos/<int:pk>/atualizar/', product_update, name='product-update'),
```
Perceba que o url recebe um **valor int igual a pk**, esse valor é chave primária do objeto que será recebido pela função update.

Para facilitar a busca pela chave primária do objeto, vamos adiconá-la no canto da tabela. Também, vamos adicionar um botão de opção, esse será para atualizar o objeto.

**product-list.html**
```html
...
{%for object in object_list%}
  <tr>
    <th>{{ object.pk }}</th> <!-- Adicionamos a pk -->
    <th>{{ object.name }}</th>
    <th>{{ object.description }}</th>
    <th>{{ object.price }}</th>
    <th>{{ object.stock_quantity }}</th>
    <th>{{ object.category.name }}</th>
    <th>
  <!-- Adicionamos um botão para atualização --> 
      <a class="btn btn-secondary" href="{% url 'product-update' object.pk %}">Editar</a>
    </th>
  </tr>
...
```
Perceba que ao usar a função url do Django, enviamos também o **object.pk** (chave primária do objeto), para que as informções desse objeto sejam recebidas pela função update e colocadas no formulário.

Agora, rode o servidor e tente atulizar algum objeto da sua tabela.

## Delete
Vamos escrever um função delete, para terminar nosso CRUD. Semelhante ao update, o delete também precisa receber uma chave primária para saber qual objeto está sendo deletedo.

**views.py**
```py
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')
    context = {'object': product, 'title': 'Excluir Produto'}
    return render(request, 'form-delete.html', context)
```
A diferença é que objeto é deletado invés de salvo. 

Note que estamos usando um formulário diferente, o **form-delete.html**. Ele é apenas umas confirmação, para que o usuário tenha certeza se vai deletar o objeto.

Vamos criar ele na mesma pasta que está o **form.html**, a pasta **templates**, pois poderemos usá-lo em outros momentos. 
```
├── templates/
    └── form-delete.html
    └── form.html
```
Se preferir, pode criar um **product-delete.html** na pasta **products**.

**form-delete.html**
```html
{%extends 'base.html'%}

{%block title%}
<title>{{title}}</title>
{%endblock%}

{%block content%}
<div class="content conatainer-fluid">
<div class="container">
  <div class="col-md-6 mx-auto my-3 border rounded-4 shadow">
    <div class="text-center h2 pt-3">{{title}}</div>

    <div class="text-center my-3 px-3">
      <form method="post" action="">
        {% csrf_token %}
        <p class="lead"> Confirme para excluir o registro definitivamente.</p>
        <p class="fs-4"> Deseja excluir: <strong>{{ object }}</strong>?</p>

        <div>
          <a class="btn btn-secondary btn-lg" href="javascript:history.back()">Voltar</a>
          <button class="btn btn-danger btn-lg" type="submit">Excluir</button>
        </div>
        
      </form>
    </div>
  </div>
</div>
</div>
{%endblock%}
```
---
Por fim, definimos a sua url e adicionamos um novo botão de opção na tabela, o botão de deletar.

**urls.py**
```py
  path('produtos/<int:pk>/deletar/', product_delete, name='product-delete'),
```
**product-list.html**
```html
...
    <th>
      <a class="btn btn-secondary" href="{% url 'product-update' object.pk %}">Editar</a>

  <!-- Adicionamos um botão para deletar -->
      <a class="btn btn-danger" href="{% url 'product-delete' object.pk %}">Excluir</a>
   </th>
...
```
Faça o teste e tente deletar um objeto da sua tabela.

Com isso, temos um CRUD completo em nosso frontend. Podemos fazer o mesmo para o outro model que criamos antes, para que não seja necessário acessar o admin do Django para adicionar novos objetos.

## ! Documento Extra -> [Crispy Forms](doc)
## Siga para o próximo documento -> [Usuário e Autenticação](/docs/autenticacao.md)
## [Acessar Sumário](../README.md#sumário)