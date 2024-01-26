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
<ul class="navbar-nav">
  ...
 
    {% if request.user.is_authenticated %}
    <form action="{% url 'logout' %}" method="post">
        {% csrf_token %}
        <button class="nav-link active" type="submit">Logout</button>
    </form>
    {% else %}
    <li class="nav-item">
        <a class="nav-link active" href="{% url 'login' %}">Login</a></li>
    {% endif %}
</ul>

<div class="me-3">
    {{ request.user }}
</div>
```
Utilizamos um form post, porque a **LogoutView** do Django pede um requisição post para o logout.

E também, o django para poder usar um IF e nele definimos dois links: Caso o usuário esteja autenticado, irá ver um link para logout. Caso contrário, irá ver um link para login.