# USANDO O CRISPY FORMS
O Crispy Forms edita automaticamente os nossos formulários, ao contrário do *forms.as_p* do Django. 

Instale o **Crispy Forms** no terminal e o **Bootstrap Crispy** para o crispy ser compátivel com a versão do Bootstrap que você está usando.
```bash
pip install django-crispy-forms crispy-bootstrap5
```
No arquivo settings.py do core do seu projeto, adicione em INSTALLED_APPS:

**settings.py**
```py
INSTALLED_APPS = [
    ...

    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
```

Para utilizar o crispy, devemos carregar sua tags em nossos templates. Por exemplo:

**form.html**
```html
<!-- No topo da página -->
{% load crispy_forms_tags %}
...

<!-- Dentro do form  -->
<form method="post" action="">
  
  {% csrf_token %}
  {{ form|crispy }}

  ...
</form>
```
Note que usamos **|crispy** ao invés de **.as_p** na tag form do Django.

Com isso, teremos formulários mais bonitos e compativéis com nosso Bootstrap.

---