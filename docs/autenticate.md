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

Lembrando que é necessário adicionar esse grupo no [admin do Django](http://localhost:8000/admin). Basta criar um grupo com nome
