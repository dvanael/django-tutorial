# LINKANDO PÁGINAS
Iremos criar novas páginas e views para nosso projeto, porém fazer a navegação delas pela barra de pesquisa do navegdor não é prático. Vamos fazer uma barra de navegação funcional.

## Criando uma nova página
Primeiro, vamos adicionar um novo HTML em nossa pasta templates. Vou chamá-lo de **about.html**, esta será nossa **página sobre** do projeto.
```
templates/
├── base.html
├── index.html
└── about.hmtl
```
Nesse HTML, vamos extender nosso **base.html** e adicionar conteúdo.

**about.html**
<!-- {% raw %} -->
```html
{%extends 'base.html'%}

{%block title%}
<title>Sobre</title>
{%endblock%}

{%block content%}
<div class="content conatainer-fluid">
<div class="container d-flex">
    <div class="mx-auto my-3 py-5 border rounded-4 shadow">
        <div class="text-center h3 my-3 p-3">
            Este projeto foi idealizado para ajudar outros alunos!
        </div>
    </div>
</div>
</div>
{%endblock%}
```
<!-- {% endraw %} -->
---
Agora é necessário **criar outra view**, assim como fizemos com o index. Logo abaixo de ``def index()``, vamos adicionar a nova função.

**views.py**
```py
def about(request):
    return render(request, 'about.html')
```
---
E adicionamos um **novo path** no **urls.py** do app.

**urls.py**
```py
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('sobre/', about, name='about'),
]
```

## Criando Links
Voltando para nosso base, vamos adicionar links na nossa navbar. Iremos utilizar a **tag url** do Django para buscar a URL que queremos. Dentro da **div da navbar** vamos adicionar no `espaço para links`.

**base.html**
<!-- {% raw %} -->
```html
...
<!-- ESPAÇO PARA LINKS -->
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-drop"  aria-controls="navbar-drop" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    
    <div class="collapse navbar-collapse" id="navbar-drop">
        <ul class="navbar-nav me-auto">
            <li class="nav-item">
                <a class="nav-link active" href="{% url 'index' %}">Início</a>
            <li class="nav-item">
                <a class="nav-link active" href="{% url 'about' %}">Sobre</a>    
        </ul>
    </div>
...
<!-- {% endraw %} -->
```
Lembrando que ``index`` e ``about`` são os name que definimos no urls.py, eles são o que realmente importa quando chamamos um url. Portanto, os defina bem para não se confundir.

Também podemos modificar os outros links do projeto, para uma navegação mais dinâmica.

---