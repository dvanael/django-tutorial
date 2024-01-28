# AUTENTICAÇÃO 
A autenticação do Django é importante porque protege as páginas da web, controla o acesso de usuários autorizados e mantém a segurança dos dados, garantindo que apenas usuários autenticados possam interagir com o sistema.

Aqui vamos começar a autenticação do sistema, para isso vamos usar as próprias views do Django, afim de facilitar o processo.

## Login e Logout
Vamos abrir o arquivo urls.py do nosso app, importar as views e crias as urls para as views.

**urls.py**
```py
from django.contrib.auth.views import *

urlpatterns = [
  ...
  # autenticação
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]
```
---
Agora vamos definir o template que será utilizado, por padrão o Django usa `registration/login.html`. Vamos criar a pasta **registration** e o **login.html** dentro da nossa pasta template.
```
templates/
├── registration/
    └── login.html
```
Vamos abrir o arquivo login.html e adicionar:

**login.html**
```html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block title %} <title>Login</title> {% endblock title %}

{% block navbar %}{% endblock navbar %}
{% block footer %}{% endblock footer %}

{% block content %}
<div class="content login container-fluid">
<div class="container py-5 my-5">
  <div class="d-flex justify-content-center align-items-center h-50">
    <div class="shadow rounded-4 border p-5 w-50 bg-white">

      <h3>LOGIN</h3>
      <form action="" method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <div class="d-flex justify-content-center">
          <button class="btn btn-success w-100" type="submit">Entrar</button>
        </div>
      </form>

    </div>
  </div>
</div>
</div>
{% endblock content %}
```
Está quase pronto, mas se você acessar a página e logar, verá que dará erro, pois será encaminhado para um endereço inexistente. Esse endereço é um padrão do Django, mas temos como alterar isso. Para isso, vamos voltar no arquivo settings.py do projeto e vamos adicionar na última linha:

**settings.py**
```py
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
```
O que estamos fazendo aqui é informar que a página que será usada para o Login é a url **'login'**, ao efetuar um login o usuário será redirecionado (redirect) para a página **'início'** e ao efetuar um logout será redirecionado para a página 'login'. 

Agora, o login do usuário está pronto e funcional.

Vamos adicionar a opção de logout. Criaremos um pequeno form post para redirecionar o usuário de volta para a página de login. Então, vamos adicionar esse form na nossa navbar.
```html
<ul class="navbar-nav me-auto">
  ...
</ul> 
<div class="d-flex align-items-center me-3">
    {% if request.user.is_authenticated %}
    <div class="nav-item">
        <div class="nav-link me-3">{{ request.user }}</div></div>
        
    <form action="{% url 'logout' %}" method="post">
        {% csrf_token %}
        <button class="btn btn-secondary" type="submit">Logout</button></form>

    {% else %}
    <div class="nav-item">
        <a class="btn btn-primary" href="{% url 'login' %}">Login</a></div>
    {% endif %}
</div>
```
Utilizamos um form post, porque a **LogoutView** do Django pede um requisição post para o logout.

Usamos um **if request.user.is_authenticated** (se o usuário está autenticado), ele renderiza "Logout", se não é renderizado o link de Login.

E também, usamos o **request.user** para mostrar o usuário que está logado.

## Autenticação
No momento, o usuário consegue logar e deslogar no sistema, mas isso não implica em nada, pois mesmo deslogado o usuário consegue ver todas as páginas. Vamos mudar isso! 

Em views.py, vamos importar:

**views.py**
```py
from django.contrib.auth.decorators import login_required
# vamos adicionar esse decorator em cada view que for necessário o login
# por exemplos

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product-list.html', {'products': products})

```
**@login_required** faz que seja necessário o **login do usuário** para acessar a página.

Lembrando que é necessário realizar isso para todas as views necessárias. Agora, caso algum usuário não logado tente acessar essa página, ele será redirecionado à página de login.

Caso você queira limitar uma página a um grupo de usuários (Ex.: professores, funcionários, administrador, etc..), você pode adicionar a seguinte função as suas views.

**views.py**
```py
from django.contrib.auth.decorators import user_passes_test

def group_required(group_name):
    def in_group(user):
        if user.groups.filter(name=group_name).exists():
            return True
        return False
    return user_passes_test(in_group, login_url='/login/')
# adicione essas função no lugar da @login_required

@group_required('<seu_grupo>')
def product_list(request):
```
**@group_required('group_name')** irá verificar se o grupo do usuário que está acessando a página pertence ao grupo definido na função. 

Lembrando que é necessário adicionar esse grupo no [admin do Django](http://localhost:8000/admin). Basta criar um grupo (não é necessário as permissões do admin) e utilizar o nome desse grupo no decorator.

Crie um grupo `admin` e um `user`.

## Acesso Negado
Caso queira, você pode adicionar uma mensagem para o usuário quando ele tentar visitar uma página que não possui acesso. Para isso, vamos trocar o que há no bloco conteúdo no arquivo login.html por:

**login.html**
```html
...
{% block content %}
<div class="content login container-fluid">
<div class="container py-5 my-5">
  <div class="d-flex justify-content-center align-items-center h-50">
    <div class="shadow rounded-4 border p-5 w-50 bg-white">

{% if request.user.is_authenticated %}
    <h3>Ação não permitida!</h3>
    <p class="lead text-bold">
      Houve algum problema para processar a ação desejada ou você não tem permissão.</p>
    <a href="{% url 'index' %}" class="btn btn-secondary"> Voltar Ao Início</a>

{% else %}
    <h3>LOGIN</h3>
    <form action="" method="post">
      {% csrf_token %}
      {{ form|crispy }}
      <div class="d-flex justify-content-center">
        <button class="btn btn-success w-100" type="submit">Entrar</button>
      </div>
    </form>
{% endif %}
    </div>
  </div>
</div>
</div>
{% endblock content %}
```
Usando **{% if request.user.is_authenticated %}**, o Django saberá se o usuário está logado e se possui acesso para aquela página. Então exibimos uma mensagem de erro e um link para o index.

Dessa forma, utilizamos a mesma página para dois propósitos diferentes.

## Filtrando por Usuário
Agora, apenas usuários cadastrados conseguem visualizar os dados sensíveis do site. Contudo, qualquer usuário consegue visualizar os dados de todos os usuários. 

Para alterar isso, precisamos criar uma relação entre os usuários e os objetos criados por ele, de forma que depois possamos filtrar os objetos para que o usuário possa apenas ver/editar/excluir os objetos que ele próprio criou. 

Vamos começar criando a **relação usuário-objeto**. Para cada classe que for necessário, adicionar como atributo:

**models.py**
```py
from django.contrib.auth.models import User # importe o usuário padrão do Django

# adicione o atributo user a classe
class Product(models.Model):
    ...
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário")

```
Como as classes foram alteradas, precisamos atualizar o banco de dados. Para isso, vamos digitar no terminal:
```bash
python manage.py makemigrations
```
Caso já haja algum cadastro no banco de dados, será necessário definir um padrão "default" para os objetos já cadastrados. 

Para isso, vamos digitar 1 (primeira opção) e vamos definir como padrão 1 (chave primária do primeiro usuário criado). Em seguida, vamos por no terminal:
```bash
python manage.py migrate 
```
Agora precisamos configurar como o usuário será associado ao objeto automaticamente.

Para cada **função create** que for necessária, vamos adicionar:

**views.py**
```py
def product_create(request):
  ...
        if form.is_valid():
            form.instance.user = request.user # vamos associar o request.user ao objeto
            form.save()
            return redirect('product-list')
            ...
```
Aqui dizemos que usuário da requisição é igual ao atributo *user* do objeto enviado no  formulário (**form.instance.user = request.user**). Assim, automaticamente, quando um usuário criar um objeto, este será associado a ele.

Agora precisamos filtrar os objetos na listagem, para que o usuário veja apenas os objetos que ele criou. Para isso, vamos modificar as **funções list**:

**views.py**
```py
def product_list(request):
    products = Product.objects.filter(user = request.user)
    return render(request, 'products/product-list.html', {'products': products})
```
Usamos **filter(user=request.user)** para que os objetos renderizados sejam aqueles associados ao usuário da requisição.

Agora resta configurar as **funções update** e **delete** para que apenas o usuário que criou o objeto possa editar/excluí-lo. Para isso, vamos adicionar no get:

**views.py**
```py
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    ...
```
No **get or error**, indetificamos que o usuário do objeto deve ser igual o usuário da requisição (**user=request.user**).
