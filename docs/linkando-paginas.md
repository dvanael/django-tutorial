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
### about.html
```html
{%extends 'base.html'%}

{%block title%}
<title>Sobre</title>
{%endblock%}

{%block content%}
<div class="container d-flex">
    <div class="mx-auto my-3 py-5 border rounded-4">
        <div class="text-center h3 my-3 p-3">
            Este projeto foi idealizado para ajudar outros alunos!
        </div>
    </div>
</div>
{%endblock%}
```

Agora é necessário **criar outra view**, assim como fizemos com o index. Logo abaixo de **def index()**, vamos adicionar a nova função.
### views.py
```py
def about(request):
    return render(request, 'about.html')
```
E adicionamos um **novo path** no **urls.py** do app.

### urls.py
```py
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('sobre/', about, name='about'),
]
```
Voltando para nosso base, vamos adicionar links na nossa navbar. Iremos utilizar a **tag url** do Django para buscar a url que queremos. Dentro da **div da navbar** vamos adicionar.

### base.html
```html
...
    <div class="navbar-collapse">
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link active" href="{% url 'index' %}">Início</a>
            <li class="nav-item">
                <a class="nav-link active" href="{% url 'about' %}">Sobre</a>    
        </ul>
    </div>
...
```
Lembrando que **index** e **about** são os name que definimos no urls.py, eles são o que realmente importa quando chamamos um url. Portanto, os defina bem para não se confundir.

Também podemos 


