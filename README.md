# Proyecto 2: Base de Datos 2

## Integrantes
* Rodrigo Céspedes
* Benjamin Diaz
* Gabriel Spranger

## Introducción
Este proyecto consiste en realizar un procesamiento de un conjunto de tweets, para posteriormente realizar una consulta de un query (e.g. “UTEC ciencia de la computación”) con el fin de retornar los tweets que tengan relación con el query. Esta página web tiene 3 funciones principales:
* Indexar: Cargar un archivo `.json` (tweets) para realizar el procesamiento y guardarlo en la base de datos.
* Query: Procesa una oración y devuelve los tweets mas relevantes al query dado. e.g. “UTEC ciencia de la computación” devolverá los tweets que hablen sobre UTEC y ciencia de la computación.
* Filtro: Recibe una oración y filtra a los tweets devueltos por la oración. Como un CTRL + F.

![alt text](images/pagina.png “Página web”)

## Construcción del índice invertido
La construcción del índice invertido se hizo principalmente en dos etapas, la primera de ellas es el preprocesamiento que se tiene que hacer al archivo .json que contiene los tweets y la construcción en sí del índice invertido e índices auxiliares
. 
La primera parte consiste en parsear el json y filtrar los tweets que nos interesan indexar, específicamente para este experimento, nosotros no tomamos en cuenta los tweets que tenían el flag de ‘retweeted’ como verdadero. Se tomó como ID de documento (docID) el campo ‘id’ y como contenido del documento el campo ‘text’ de cada entrada del json. Esta primera parte del preprocesamiento se hace dentro de la función read_json().  Luego, tenemos que filtrar del contenido del documento las palabras que nos interesa indexar, para esto se realiza una filtración donde se tokenizan los términos dentro del texto, se remueven los stop words y se realiza un stemming de las palabras resultantes, esta filtración se hace dentro de la función limpiar_texto(). Luego, todas estas se agregan al conjunto total de palabras de todos los tweets



## Manejo de memoria secundaria


## Ejecución de las consultas


