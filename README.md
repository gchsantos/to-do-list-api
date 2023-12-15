
# ToDo List!


Olá! Meu nome é Gabriel Cesar Hilario dos Santos, dono do presente projeto. Através desse ReadMe farei o possível para que você consiga subir toda a estrutura desenvolvida para o desafio de forma simples e eficiente (Com apenas um comando 😉)!

  
# Sobre a API

Esta API foi solicitada por meio de um desafio técnico pela equipe de Recrutamento e Seleção da Greenole, tem como principal funcionalidade o gerenciamento das tarefas do usuário autenticado.

  
# Clonando O Repositório

Primeiramente, teremos que clonar o repositório, dessa forma todos os arquivos necessários para o funcionamento do projeto ficarão armazenados em um diretório local. Para isso é só executar o seguinte comando no seu terminal:

    git clone git@github.com:gchsantos/to-do-list-api.git

  # Criando variável de ambiente
  
Será necessário criar um arquivo **.env** no diretório raiz da aplicação, para isso acesse o diretório do repositório:

    cd to-do-list-api
    
Logo após crie o arquivo **prod.env** com as seguintes variáveis:

    SECRET_KEY=django-insecure-&qs66ex^&g70=gc@pjucoy0r$=#&*=zapxt^qc2v7rk-yet_o%
    POSTGRES_USER=gchsantos
    POSTGRES_PASSWORD=itawesome
    POSTGRES_DB=to_do_list_db
    DATABASE_HOST=postgres
    TZ=America/Sao_Paulo
    REDIS_PASSWORD=itawesome
    REDIS_LOCATION=redis://:${REDIS_PASSWORD}@cache:6379


# Subindo o ambiente 😉
Chegamos na melhor parte do projeto! Como estamos utilizando o querido ***docker-compose***, precisaremos apenas de um único comando para termos todo o ambiente em funcionamento. Continue dentro do repositório (**pasta clonada**) e execute o seguinte comando:
 
    docker-compose up -d

## Postgres

Após subirmos a estrutura, surgirá um *container* chamado **to-do-list-api-postgres-1** este que é responsável pelo banco de dados [PostgreSQL](https://www.postgresql.org/about/) da API.


## API

A API surgirá com o *container* denominado **to-do-list-api-postgres-1**, é nela que iremos realizar as nossas requisições para interagir com a solução.

### Autenticação

Para obtermos autorização e garantirmos que somente pessoas autenticadas possam realizar requisições importantes dentro da API precisaremos **criar um usuário**, execute o seguinte comando em seu terminal:

    curl -X 'POST' \
	  'http://localhost:8000/account/register' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -H 'X-CSRFTOKEN: 8dBoGBQhQ7uSRsAGucJMTnn4mOaflaGluHyyngwVhb4eVLiqt5btjUQbHFJEPwVm' \
	  -d '{
	  "username": "sogeking",
	  "password": "lockon",
	  "is_superuser": true
	}'
 
**Você irá obter o seguinte retorno (200):**

```json
{"username":"sogeking","is_superuser":true}
```

**Agora iremos autenticar o usuário criado para que ele receba um Token liberado para realizar as requisições:**

	   curl -X 'POST' \
	  'http://localhost:8000/account/auth' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -H 'X-CSRFTOKEN: 8dBoGBQhQ7uSRsAGucJMTnn4mOaflaGluHyyngwVhb4eVLiqt5btjUQbHFJEPwVm' \
	  -d '{
	  "username": "sogeking",
	  "password": "lockon"
	}'

  
**Seguindo os passos desse tutorial você obterá o seguinte retorno da API você irá obter um retorno parecido com esse:**

```json
 {"token": "9b24c7354e91c2ce4cfb619cacb5affaa3ed4ade"}
```

✨ **Pronto!** ✨ Agora já temos acesso as requisições da API, **guarde o *token* retornado** para as próximas requisições.


## Documentação da API

**Agora tá na hora de brincar um pouquinho com as funcionalidades da API!**

Para acessar a documentação contendo os *endpoints* é só [clicar aqui!](http://localhost:8000/api/schema/swagger-ui/)

**Vale lembrar que para podermos testar o banco de dados em cache de maneira rápida, o tempo de atualização dos dados foi ajustado para 30 segundos!**

Muito obrigado! Qualquer dúvida este é meu contato: gchsantos@gmail.com
