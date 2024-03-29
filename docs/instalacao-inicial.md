# INSTALAÇÃO INICIAL 
Primeiro instale o [Python](https://www.python.org/downloads/). Deve-se marcar a opção de adicioná-lo ao PATH durante a instalação para que ele possa ser acessado de qualquer pasta do computador.

## Instale o VS Code
Instale o [VSCode](https://code.visualstudio.com/download). Algumas extensões úteis que podem ser baixadas no próprio VSCode:
- Python
- Django
- IntelliSense
- jQuery code snippets

Crie uma pasta para seu projeto.

É nessa pasta onde iremos trabalhar com nosso projeto. Abra a pasta com o **VS Code**.

## Crie um ambiente virtual
Abra um terminal na pasta do seu projeto e crie um ambiente virtual.

No terminal, digite:
``` bash
python3 -m venv venv 
```

**Ative o ambiente virtual**, digite no terminal:

- No Windows:
    - ` venv\Scripts\activate `

- No Linux:
    - ` source venv\Scripts\activate `

Para **desativar** o ambiente virtual, digite:
``` bash
deactivate
```
>**ATENÇÃO**: nunca reutilize seu venv, crie um em cada máquina que usar.

___
## Utilizando o requirements.txt
Em nosso projeto, iremos fazer várias instalações ao decorrrer de sua programação. Essas instalações se tornaram dependências para rodar nosso projeto. O próprio Django sendo uma delas.

Vamos fazer um arquivo que irá registrar essas dependecias, facilitando a instalação das mesmas em outros ambientes de desenvolvimento ou produção.

Execute esse comando no desenvolvimento para registrar novas instalações. No terminal, digite :
```bash
pip freeze > requirements.txt
```

Para instalar as dependências em outro ambiente. Execute:
```bash
pip install -r requirements.txt
```
---