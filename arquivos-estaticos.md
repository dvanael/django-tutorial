# ARQUIVOS ESTÁTICOS
Arquivos estáticos são arquivos que são enviados ao navegador exatamente como estão no HD do servidor, ou seja, sempre serão os mesmos, não sofrendo alterações. Exemplo disso seriam arquivos de imagem, CSS e JavaScripts.

## Criando a pasta static
Vamos criar na pasta do nosso projeto uma pasta chamada **static** (padrão do Django) e mais uma pasta para cada tipo de arquivo, seguindo o seguinte modelo:
```
<pasta_do_projeto>/
├── core/
├── <pasta_do_app>/
└── static
    ├── css/
    ├── img/
    └── js/
```

## Configurando o static
Agora precisamos indicar ao nosso projeto onde a pasta está localizada. Para isso, vamos abrir o arquivo **settings.py** e buscar por **STATIC_URL**, adicionando logo após:
```py
STATIC_URL = '/static/'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
```

Para testar, vamos criar na **pasta css** um arquivo **styles.css**. Nele vamos colocar:
```css
body{
    background-color: lightblue;
}
```

Em **index.html** vamos adicionar duas linhas de código.
```html
{% load static %} <!-- para carregar o static que configuramos  -->

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Página Inicial</title>

    <link rel="stylesheet" href="{% static 'css/styles.css' %}"> <!-- indicando onde está nosso arquivo styles.css no static -->
</head>
<body>
    <h1>Bem vindos ao meu Projeto Django!</h1>
</body>
</html>
```

Se atualizarmos nossa página inicial, devemos vê-la com uma cor de fundo diferente do branco padrão.