10 DE JULHO, 2022 [**#4**]

---

## Introdução

Neste artigo não irei me estender muito na parte de configuração e o processo de deploy na `AWS Lambda` como um todo, irei apenas disponíbilizar um script para automatizar esse processo e com certeza deixar tudo mais rápido.

Para este exemplo iremos utilizar outro serviço da AWS chamado `Amazon S3` que é basicamente um local para armazenamento de arquivos de qualquer tipo. Esse serviço disponíbiliza acesso a 5GB de armazenamento por 12 meses no nível gratuíto. É no S3 onde iremos realizar o upload do projeto para uso no Lambda.

**Requerimentos do Sistema**

```
sudo apt install zip
sudo apt install awscli
```

#### Zip Package

Comprimir nossa aplicação em um arquivo .ZIP

```
mkdir zip && cp -r app/ zip/app/ && cp -r config.py zip/config.py \
&& cd $venv_dir && zip -r9 "$root_dir/$file_name" . \
&& cd "$root_dir/zip" && zip -g ../$file_name -r . \
&& cd "$root_dir" && rm -r zip
```

#### Upload S3

Realizar o upload do nosso arquivo .ZIP para o S3.

```
cd $root_dir \
&& aws s3 cp $file_name s3://$bucket_name/$file_name
```

#### Update Function Lambda

Atualizar a função Lambda com a última versão.

```
aws lambda update-function-code --function-name $function_name --s3-bucket $bucket_name --s3-key $file_name
cd $root_dir
rm -r $file_name
```

#### Modelo Básico de Estrutura de API

```
projects/
│
├── app/
│   │
│   │
│   └── api/
│       ├── __init__.py
│       └── main.py
│
├── config.py/
│
└── vemv/
```

#### Script Completo

```
#!/usr/bin/env bash
root_dir=$PWD
venv_dir="$root_dir/venv/lib/python3.9/site-packages"
function_name="app-api-dev"
bucket_name="app-api"
file_name="app_dev.zip"

# Zip Package
mkdir zip && cp -r app/ zip/app/ && cp -r config.py zip/config.py 
&& cd $venv_dir && zip -r9 "$root_dir/$file_name" . 
&& cd "$root_dir/zip" && zip -g ../$file_name -r . 
&& cd "$root_dir" && rm -r zip

# Upload S3
cd $root_dir 
&& aws s3 cp $file_name s3://$bucket_name/$file_name

# Update Function Lambda
aws lambda update-function-code --function-name $function_name --s3-bucket $bucket_name --s3-key $file_name
cd $root_dir
rm -r $file_name
```


**Mais informações**

- [Github Gist Source Code](https://gist.github.com/FernandoCelmer/8e2bc511ab8e1bff2059cd5c77a33776)