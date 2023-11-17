# Web Scraping de Perfumes - Projeto Fragrância
Bem-vindo ao repositório do projeto de web scraping de perfumes, dedicado ao site Fragrância. Este projeto tem como objetivo extrair informações significativas sobre marcas e links de perfumes disponíveis no site para análises futuras. Embora o projeto esteja em andamento, as informações sobre marcas de perfumes e links de perfumes já estão disponíveis na raiz deste repositório.

## Conteúdo do Repositório
- **load_perfumes_to_scrape.py** (Em desenvolvimento): Este script realiza a extração de dados sobre perfumes do site Fragrância. Lembre-se de adicionar sua API_KEY do ScraperApi no arquivo para garantir a execução sem problemas.

- **main.py**: Este script realiza o scrapping de dados para dos links dos perfumes e suas marcas.  O csv com os dados obtidos estao disponiveis na raiz do repositorio.

- **brands.csv**: Contém informações sobre todas as marcas de perfumes disponíveis no site.

- **perfume_links.csv**: Apresenta os links de todos os perfumes encontrados no Fragrância.

- **mongo.py**: Este arquivo inclui a funcionalidade para adicionar links ao banco de dados MongoDB. Confira as instruções abaixo para configurar a conexão corretamente.

## Configuração do ScraperApi

Em todo o código, a plataforma ScraperAPI é utilizada, sendo necessário o uso de uma API_KEY. Para cada trecho de código em que você for utilizar, modifique-o da seguinte forma:
```python
API_KEY = "SUA_API_HEY"
```

## Configuração do MongoDB

O arquivo mongo.py fornece funcionalidades para adicionar links ao banco de dados MongoDB. Siga as instruções abaixo para configurar a conexão:

1. Instalação do MongoDB: Certifique-se de ter o MongoDB instalado em seu sistema.

2. Configuração do Banco de Dados: Abra mongo.py e ajuste as configurações do banco de dados, como nome do banco de dados, coleção, host, e porta.

```python
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "COLOQUE SUA DATABASE AQUI"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   db = MongoClient(CONNECTION_STRING)['perfume']
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return db
```

## Instruções para Executar o Programa
1. **Baixar as Dependências:**
Certifique-se de ter o Python e o pip instalados em seu ambiente. Em seguida, execute o seguinte comando para instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

2. **Obter links dos perfumes:**
Utilize o comando abaixo para carregar no seu MongoDB as informacoes com os links dos perfumes, ou carregue diretamente utilizando o CSV na raiz do repositorio.

```bash
python web_scraping/main.py
```

3. **Obter Informações dos Perfumes (A Fazer/Não Está Pronto):**
Execute o arquivo main.py para obter as informações detalhadas dos perfumes. Esta funcionalidade ainda está em desenvolvimento e não está pronta para uso. Aguarde atualizações futuras para utilizar esta etapa.
