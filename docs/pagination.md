# PAGINAÇÃO
A paginação é essencial para lidar com grandes quantidade de dados em um sistema, esses conjuntos de dados são separados em páginas, tornando mais fácil a visualização e navegação entre esses dados. 

Caso a quantidade de dados seja muito grande, o tempo que a página web irá levar para baixar todos eles será muito alto, o que não é o ideal. 

Então, utilizando a paginação, apenas uma parcela dos dados será transferida do banco de dados para a página web, melhorando o desempenho e usabilidade.

## Criando a Paginação
Nas views do nosso app, vamos importar o ``Paginator`` do Django. Vamos procucar nossa **função list** e adicionar: 

> **ATENÇÃO**: Se você está está usando usuários para filtra os objetos renderizados, como visto em **Autenticação**, aplique esse filtro antes da paginação.

**view.py**
```py
from django.core.paginator import Paginator
...

def product_list(request):
    products = Product.objects.all() # ou filtro por usuário
    paginator = Paginator(products, 5)  #5 objetos por página

    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    context = {
      'page': page_objects
    }
    return render(request, 'products/product-list.html', context)
```
Com o ``Paginator`` informamos quais os conjuntos de dados, nesse caso ``products``, e a quatidade de dados por página.

O ``page_number`` utiliza o ``get('page')`` para buscar a página atual, um parâmetro que vem através da url. Por exemplo, ``/produtos/?page=2`` é a segunda página de produtos.

O ``page_objects`` pega a página atual, buscada pelo ``page_number``. Desta forma, é feita a listagem dos dados específiocos (``paginator``) daquela página (`page_number`).

Passamos esses dados como ``'page'`` no contexto do nosso template. Vamos atualizar nosso ``object_list`` no template para que a paginação começe a funcinar.

**product-list.html**
<!-- {% raw %} -->
```html
{% for object in page.object_list %}
```
<!-- {% endraw %} -->
Aqui usamos ``page`` como nossa lista de objetos renderizados no template.

Agora podemos acessar o link da listagem e veremos apenas 5, caso haja mais do que isso. Para acessar as páginas seguintes, nós podemos digitar na barra de navegação:

- [localhost:8000/produtos/?page=1](http://localhost:8000/produtos/?page=1)
- [localhost:8000/produtos/?page=2](http://localhost:8000/produtos/?page=2)
- [localhost:8000/produtos/?page=3](http://localhost:8000/produtos/?page=3)

Crie novos objetos, se necessário, par testar a páginação.

---
Porém, a navegação pela barra de pesquisa não é prática para o usuário. Vamos criar links para a páginação. Logo abaixo da nossa tabela, vamos adicionar:  

**product-list.html**
<!-- {% raw %} -->
```html
  <div class="table-responsive">
    ...
  </div>  

  <nav>
    <ul class="pagination justify-content-center">
      {% if page.has_previous %}
        <li class="page-item">
          <a class="page-link" href="?page=1">Primeiro</a>
        </li>

        <li class="page-item">
          <a  class="page-link" href="?page={{ page.previous_page_number }}">Anterior</a>
        </li>
      {% endif %}

      <li class="page-item">
        <span class="page-link current">
          Página {{ page.number }} de {{ page.paginator.num_pages }}
        </span>
      </li>
      
      {% if page.has_next %}
        <li class="page-item">
          <a class="page-link" href="?page={{ page.next_page_number }}">Proxímo</a>
        </li>

        <li class="page-item">
          <a class="page-link" href="?page={{ page.paginator.num_pages }}">Último</a>
        </li>
      {% endif %}
    </ul>
  </nav>
```
<!-- {% endraw %} -->
Estamos agora fornecendo links de paginação para navegar facilmente entre as páginas de resultados.

---
## Campos de Busca
Adicionar um campo de busca é uma funcionalidade útil que permite aos usuários filtrar os objetos e localizar informações com mais facilidade. Para implementar isso, precisamos fazer algumas modificações em nossa **list view**.

**views.py**
```python
def product_list(request):
    products = Product.objects.all()
    # Processa o parâmetro de busca 'n'
    name = request.GET.get('n', '') 
    if name:
        # Filtra os produtos com base no nome fornecido
        products = products.filter(name__icontains=name)

    # Pagina os produtos
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    # Adiciona os produtos paginados e o termo de busca ao contexto
    context = {
        'page': page_objects,
        'name': name,
    }
    return render(request, 'products/product-list.html', context)
```
Quando o usuário envia o formulário de busca, o parâmetro `n` é enviado para a view. A view então filtra os objetos com base nessa consulta.

No template `product-list.html`, temos um formulário com um campo de entrada de texto para o usuário inserir o termo de busca.

**product-list.html**
<!-- {% raw %} -->
```html
  <form class="filter d-md-flex" action="?" method="GET">
    <div class="btn-group" role="group">
      <input class="rounded-start border border-3 ps-2" type="text" name="n" value="{{name}}" placeholder="Pesquise...">
      <button class="btn btn-success" type="submit">Buscar</button>
      <a class="btn btn-secondary rounded-end" href="?">Limpar</a>
    </div>
  </form>
```
<!-- {% endraw %} -->
Ao clicar no botão de busca, o texto é adicionado à URL como um parâmetro. Por exemplo, se buscarmos por "info", o link será `produtos/?n=info`.

A busca funciona da seguinte forma:
1. O valor do campo de entrada de texto com `name="n"` é enviado para a URL.
2. A view obtém o valor de `n` da URL e filtra os produtos com base nesse valor.
3. Os objetos filtrados são enviados para o template.

O valor do campo de entrada `value` é preenchido com `{{name}}` do contexto, permitindo que o termo de busca continue no campo após recarregar a página.

Porém, ao mudar de página, o termo de busca é perdido. Para resolver isso, precisamos incluir o termo de busca em cada link de paginação.

<!-- {% raw %} -->
```html
<a href="?page={{ ... }}&n={{name}}">
```
<!-- {% endraw %} -->

Aqui, estamos adicionando dois parâmetros para cada link: `page` representa o número da página e `name` representa o termo de busca. Esses parâmetros são separados por `&`. Dessa forma, o termo de busca será mantido durante a navegação por páginas.

___
## Filtros
Para buscas mais completas podemos adicionar outras buscas e filtros. Por exemplo, vamos usar um ``input select`` para filtrar nossos objetos usando informações do nosso banco de dados.

**views.py**
```py
def product_list(request):
    ...
    # Adicionamos as categorias 
    categories = Category.objects.all()
    # Busca a cateria enviada para a URL
    category =  request.GET.get('category','')
    if category:
      # Filtra com base na categoria selecionada
        products = products.filter(category__name__icontains=category)

    ...

    # Adiciona no contexto as categorias e a cateria selecionada 
    context = {
        'page': page_objects,
        'name': name,
        'categories': categories,
        'category': category,
    }
    return render(request, 'products/product-list.html', context)
```
Segue a mesma lógica da busca feita anteriormente.

Agora temos os dados enviados ao template, vamos usá-los para criar nosso campo ``select``, logo abaixo do nosso campo de busca.

**product-list.html**
<!-- {% raw %} -->
```html
  <form class="filter d-md-flex" action="?" method="GET">
      ...

    <div class="btn-group ms-lg-3" role="group">
      <select class="form-select rounded-start rounded-0 border border-3" name="category"> 
          <option value="">Todas as categorias</option>
          {% for category in categories %}
              <option value="{{category.name}}"
                {% if request.GET.category == category.name %}selected{% endif %}>
                  {{category.name}}
                </option>
          {% endfor %}
      </select>
      <button class="btn btn-success" type="submit">Filtrar</button>
    </div>
    
</form>
```
<!-- {% endraw %} -->
Aqui listamos as categorias no ``option`` do ``select``, para evitar erros conferimos o parâmetro ``category`` da URL e comparamos com o ``category.name`` para deixar a categoria selecionada.

Lembrando que temos que adicionar esse parâmetro nos **links de páginação** também.

<!-- {% raw %} -->
```html
<a href="?page={{ ... }}&n={{name}}&category{{category}}">
```
<!-- {% endraw %} -->
___

## Múltiplas Buscas
É possivel usar apenas um campo para filtrar diferentes atributos dos objetos. Por exemplo, buscando por nome e descrição do objeto. Você pode realizar utilizando filtros ``Q`` (queries) combinados.

Os objetos ``Q`` em Django permitem criar consultas mais complexas, permitindo a combinação de consultas usando operadores lógicos como **AND**, **OR** e **NOT**.

Com um campo de busca já feito, basta adicionar em sua view:

**views.py**
```py
from django.db.models import Q
...

def product_list(request):
    products = Product.objects.all()
    ...
    
    name = request.GET.get('n', '')
    if name:
    # Filtra tanto o nome quanto a descriçãp, com base no mesmo valor
        products = products.filter(
          Q(name__icontains=name) | 
          Q(description__icontains=name)
        )
    
    ...
```

Você pode ajustar este exemplo de acordo com a estrutura do seu modelo e os atributos pelos quais deseja realizar a busca. Isso permite que os usuários realizem pesquisas de vários atributos com um único input.

---