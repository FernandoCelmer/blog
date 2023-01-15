20 DE FEVEREIRO, 2022 [**#01**]

---

## Introdução

Docker é uma ferramente opensource escrito em GO para gerenciamente e criação de containers.

**Servidor Físico / Máquina Virtual / Container**

Servidor é uma máquina física qualquer onde você instala um sistema operacional baseado em linux. Quando é maquina virtual, você executa um novo sistema operacional dentro do seu sistema operacional que já esta sendo executado na sua maquina física. O container não precisa rodar um novo sistema operacional dentro do sistema operacional da minha maquina física. Quando é utilizado uma maquina virtual, ela contem o seu próprio kernel, as suas próprias bibliotecas etc. Em um container não, quando eu estou utilizando o container, somente o processo que eu pedir vai estar em execução. As bibliotecas e os binarios, ele compartilha da maquina host.

#### Comandos Básicos

- Faz a listagem dos containers que estão ativos no momento.
```
$ sudo docker ps
```
___

- Com o parâmetro -a é feito a listagem de todos os containers inativos.

```
sudo docker ps -a
```
___

- Cria um novo container com ubuntu. Pode ser colocado parametros adicionais como a porta que vai ser redirecionado esse container.

```
sudo docker run -i -t -p 8080:80 ubuntu:14.10
```
___

- Para a execução de um container.

```
sudo docker stop CONTAINER_ID
```
___


- Cria uma imagem. O bom é sempre realizar o versionamento da imagem criada recentemente.

```
sudo docker commit CONTAINER_ID [qualquer_nome:1.0]
```
___

- Executa comandos dentro do conteiner.

```
sudo docker exec CONTAINER_ID [command]
```
___

- Conecta a um terminal linux dentro do container.

```
sudo docker exec CONTAINER_ID /bin/bash
```
___


- Retorna informações sobre determinado container.

```
sudo docker inspect CONTAINER_ID
```
___

- Com esse comando eu consigo ver o quanto o meu container esta consumindo de CPU, memória RAM e rede.

```
sudo docker stats CONTAINER_ID
```
___

#### Diferenças

**Dockerfile**

- Dockerfile configura as imagens para um container.

**Docker-Compose**

- Docker-compose configura as imagens para os containers e a conexão entre eles.

---

**Mais informações**

- [Docker Getting Started](https://docs.docker.com/compose/gettingstarted/)
- [Diferença entre o Dockerfile e o Docker-Compose](https://cursos.alura.com.br/forum/topico-diferenca-entre-o-dockerfile-e-o-docker-compose-30250)