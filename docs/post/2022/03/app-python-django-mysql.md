02 DE MARÇO, 2022 [**#03**]

---

## Introdução

Nesse tutorial vamos nos concentrar nessas cinco tecnologias abaixo para o desenvolvimento do nosso pequeno projeto de teste:

- Linux
- Python 3.9
- Django 4.0
- AWS Elastic Beantalk
- MySQL

## 1 — Estrutura Inicial

#### Criação ambiente de desenvolvimento:

Vamos começar pelo mais básico de tudo que é criar nosso ambiente de desenvolvimento utilizando o virtualenv com os seguintes comandos abaixo. Estou trabalhando com sistema operação linux, distribuição Kubuntu, especificamente Ubuntu versão 21.10.

```
$ mkdir projects
$ cd projects
$ virtualenv -p python3.9 venv
$ source venv/bin/activate
```

Para simplificar e deixar mais organizado eu criei um novo diretório no meu computador chamado `projects` onde será colocado o meu novo projeto. Essa etapa se você quiser pode pular e colocar o seu projeto em qualquer lugar.

#### Instalação dos Requerimentos

Esses são os requerimentos básicos para o nosso projeto funcionar tranquilamente. Após executar a instalação dos pacotes não se esqueça de gerar o arquivo de requerimentos do sistema.

```
(env) $ pip install django==4.0
(env) $ pip install django-environ==0.8.1
(env) $ pip install mysqlclient==2.1.0
(env) $ pip install gunicorn==20.1.0
```

#### Criação Estrutura do Projeto Django

```
(env) $ django-admin startproject application
(env) $ cd application
(env) $ python manage.py startapp hello
```

Se você chegou até aqui, muito bem! Então a sua aplicação deverá ter essa estrutura de pastas representadas aqui em baixo.

```
projects/
│
├── application/
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── hello/
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └──  views..py
│   ├── manage.py
│
└── vemv/
```

Nesse ponto, a nossa aplicação já pode ser executado local, colocando o seguinte comando `python manage.py runserver` no seu terminal.

Como nós ainda não realizamos a configuração do Banco de Dados **MySQL**, o **Django** traz configurações padrão para o banco de dados sqlite. Então ao executar a aplicação, será gerado automaticamente um arquivo `db.sqlite3` dentro do projeto.

Nessa primeira execução você verá uma mensagem de alerta em vermelho representado na **Imagem-01**.

<center>

![Imagem-01 - Terminal](x_img_03_01.png)

**Imagem-01 - Terminal**

</center>

IMAGEM-01 — Mensagem de alerta: You have 18 unapplied migration(s).
> You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, > auth, contenttypes, sessions. Run ‘python manage.py migrate’ to apply them.

Esse alerta quer dizer que à 18 (dezoito) migrações não aplicadas no seu projeto. Essas migrações são referente ao painel padrão de administração do **Django**. Para testar, podemos executar o comando `python manage.py` migrate para ser aplicado todas as migrações de tabelas do painel de controle do **Django**. Enquanto não configuramos nosso banco **MySQL**, essas migrações serão aplicados localmente no nosso banco **sqlite**.

<center>

![IMAGEM-02 — Página inicial Django](x_img_03_02.png)

**IMAGEM-02 — Página inicial Django**

</center>

#### Criação das Variáveis de Ambiente (Arquivo .env)

As variáveis de ambiente são uma peça chave para o nosso projeto ser bem estrutura e também ter um nível básico de segurança. É nas nossas variáveis de ambiente que ficam guardadas informações criticas da aplicação como por exemplo, acesso ao banco de dados, senhas, chaves privadas. Vamos criar um arquivo `.env` com as seguintes configurações:

> PATH — /projects/application/.env

```
DJANGO_DEBUG=True
DJANGO_ENV=development
DJANGO_DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
DJANGO_SECRET_KEY=key
DJANGO_HOST=0.0.0.0
DJANGO_PORT=8080
DJANGO_ALLOWED_HOSTS=localhost
DISABLE_COLLECTSTATIC=1
```

#### Implementação arquivo de Configuração Django

Vamos fazer algumas alterações no arquivo `settings.py` para que o projeto fique adequado para deploy em um ambiente de produtoção. Então abra o arquivo no seu editor de texto preferido e adicione as seguintes linhas:

> PATH — /projects/application/application/settings.py

```
import os
from pathlib import Path
APP_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
```

Substitua as variaveis com informações sensíveis para buscar esses dados no arquivo `.env` e não diretamente no código fonte.

```
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [os.getenv("DJANGO_ALLOWED_HOSTS")]
```

Altere as configurações de templates, adicionando um caminho padrão para a aplicação.

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(CONTENT_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### Gerando StaticFiles

Crie um nova pasta dentro do diretório da aplicação chamado `content .` Esse será o local onde estará os nossos arquivos estáticos do projeto.

> PATH — /projects/application/content PATH — /projects/application/content/assets

```
(venv) $ cd project/application
(venv) $ mkdir content
(venv) $ cd content
(venv) $ mkdir assets
```

Após criar a pasta `content`, volte para o arquivo de configuração `settings.py` e faça mais algumas implementações.

> PATH — /projects/application/application/settings.py

```
STATIC_ROOT = os.path.join(CONTENT_DIR, 'staticfiles')
STATIC_URL = '/content/static/'
MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media')
MEDIA_URL = '/content/media/'
STATICFILES_DIRS = [
    os.path.join(CONTENT_DIR, 'assets'),
]
LOCALE_PATHS = [
    os.path.join(CONTENT_DIR, 'locale')
]
```

Se você terminou essa parte, então já consegue executar o comando para geração dos arquivos estáticos `python manage.py collectstatic`.

#### Configuração Procfile - (Conf AWS)

> PATH — /projects/application/Procfile

Antes de iniciar adicionar o nosso arquivo de configuração para AWS, vamos instalar um cara chamado gunicorn com o seguinte comando `sudo apt install gunicorn`. Gunicorn (‘Green Unicorn’) é um servidor WSGI para Unix feito em Python puro. Ele não tem depedências e é fácil de instalar e usar.

Crie um novo arquivo chamado Procfile no mesmo nível em que está o arquivo `manage.py` e adicione a seguinte linha de código que está abaixo:

```
web: gunicorn application.wsgi:application --log-file - --log-level debug
```

#### Geração de Requirimentos da aplicação

> PATH — /projects/application/requirements.txt

```
(env) $ pip freeze > requirements.txt
```

## 2 — Banco de Dados

#### Criando um Banco de Dados MySQL Grátis

Primeiro acesse o link [db4Free](https://www.db4free.net/) para criar uma conta gratuitamente e ter acesso a um banco de dados **MySQL** para teste. O cadastro é bem simples, basta preencher as informações básicos do banco como Nome do banco, Nome de usuário, Senha e E-mail.

<center>

![IMAGEM-03 — Página de Cadastro db4free](x_img_03_03.png)

**IMAGEM-03 — Página de Cadastro db4free**

</center>

Após preencher todas as informações é só clicar em **Cadastre-se** e verificar o seu e-mail na sua caixa de entrada. Lá você receberá informações adicionais de conexão ao banco e de como acessa-lo posteriormente pelo **PHPAdmin**.

<center>

![IMAGEM-04 — Página db4free após a realização do cadastro](x_img_03_04.png)

**IMAGEM-04 — Página db4free após a realização do cadastro**

</center>

#### Configurando Django + MySQL

Para realizarmos configuração da conexão do banco de dados **MySQL** vamos utilizar um pacote chamado `dj_database_url`. Antes de tudo podemos instalar ele com o comando descrito abaixo e também podemos adiciona-lo em nosso arquivo de requerimentos.

```
(env) $ pip install dj-database-url==0.5.0
```

Após realizar a instalação do pacote, vamos editar o arquivo settings.py, para realizar a importação de `dj_database_url`.

> PATH — /projects/application/settings.py

```
import dj_database_url
```

E adicionamos também esse trecho de código que realiza a inserção da URL do banco de dados de acordo com as informações que estão no nosso arquivo .env no parametro `DJANGO_DATABASE_URL`.

```
DATABASES = {
'default': dj_database_url.config(default=os.getenv("DJANGO_DATABASE_URL"))
}
```

Quando você terminar de adicionar essas configurações acima, podemos testar novamente a aplicação executando o comando para realizar as migrações `python manage.py migrate` do banco de dados no novo host **MySQL**.

<center>

![IMAGEM-05 — Resultado do comando python manage.py migrate.](x_img_03_05.png)

**IMAGEM-05 — Resultado do comando python manage.py migrate.**

</center>

<center>

![IMAGEM-06 — Visualização no PHPAdmin das tabelas padrão do Django.](x_img_03_06.png)

**IMAGEM-06 — Visualização no PHPAdmin das tabelas padrão do Django.**

</center>

Show! Agora o nosso projeto django já está com a configuração básica para funcionar em produção.

---

**Mais informações**

- [Github Project](https://github.com/FernandoCelmer/project-django-aws-elastic-beanstalk)