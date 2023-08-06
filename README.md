# Crear y actualizar dataset de páginas web extraidas.

Extrae información de páginas web relacionadas a partir de un conjunto inicial. Se aplican filtros con [regex](https://docs.python.org/3/library/re.html) para excluir e incluir palabras específicas. El scraping se realiza con [asyncio](https://docs.python.org/3/library/asyncio.html) y [httpx](https://www.python-httpx.org/). En dos fases. Primero se extrae toda la información de las páginas web, luego se realiza una busqueda de páginas web adicionales. La forma de detener el algoritmo es con un tope de páginas máximas a visitar o cuando ya no encontró nuevas páginas que cumplieran con las reglas de regex definidas.

## Instalación.
- [Python.](###Python)
- [Docker.](###Docker)

### Python
*Se recomienda configurar un entorno virtual con [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) o cualquier otra herramienta con este propósito.*

Una vez descargado el código. Instalar librerias necesarias.
```bash
pip install -r requirements.txt
```
### Docker
***Al utilizar [Docker](https://www.docker.com/) se garantiza que se ejecute de manera coherente en diferentes entornos. Además, Docker facilita la escalabilidad y la gestión de recursos, permitiendo ejecutar múltiples contenedores en una misma máquina. Sin embargo, puede requerir más recursos y complejidad al configurar la infraestructura y necesita ciertos conocimientos para su correcta implementación y seguridad. En general, Docker simplifica la implementación y distribución de aplicaciones.***

[Instalar Docker](https://www.docker.com/products/docker-desktop/)

Construir imagen.
```bash
docker build -t scraping .
```

## Cómo utilizarlo.
Al ejecutar el código se pueden utilizar dos modos según sea la función deseada, crear o actualizar. Estos modos se eligen por medio de banderas. Es importante saber que estos dos modos estan configurados en base a dos constantes dentro del paquete `create_data_set` en el archivo `constantes.py`.


### Python
Crear base de datos.
```bash
python .\src\run.py -c
```
Actualizar base de datos.
```bash
python .\src\run.py -u
```
### Docker
Crear base de datos.
```bash
docker run --rm -it chatenv -c
```
Actualizar base de datos.
```bash
docker run --rm -it chatenv -u
```

## Guia de carpetas.
### data
En esta carpeta se encuentra toda la información de las páginas extraidas en formato *.json*
### logs
Almacena los registro obtenidos durante la creación del conjunto de datos como el rendimiento, las páginas visitadas y los errores obtenidos.

Para checar el rendimiento del código se hace uso de la libreria `snakeviz`:
```bash
snakeviz logs/fecha/archivo.prof

```

### models
Se guardan todos los modelos entrenados a partir de los datos. Estos modelos serán guardados en formato `pickle` y para utilizarlos se debe crear un [paquete](https://realpython.com/python-modules-packages/) en python con los la clase del modelo `tfidf.py`, los datos que corresponden a ese modelo y el modelo mismo en formato *.pickle*

### src
El codigo principal y dentro el subpaquete `create_data_set` que involucra tanto su creacion como actualización. Dentro de src existe un archivo `database.py` que iba ser utilizado para generar una base de datos a partir de los datos extraídos con [Chroma](https://www.trychroma.com/), pero, se descartó la idea debido al alto consumo de recursos y la nula mejora. No se eliminó el archivo con la intención de funcionar como template para otro tipo de base de datos en caso de que se considere viable.
## Ejemplo.

Datos:
```
[
    {
        "document": " Coordinación de enseñanza..."
        "metadata": {
            "keywords":"palabra1, palabra2, ..."
            "url": "https://www.pagina.izt.uam.mx"
        }
    }
]
```
Rendimiento:
![Captura de pantalla 2023-08-06 005747](https://github.com/ivanhue/scraping_urls/assets/47096604/1d69b6e9-c244-4481-ae49-3d9617596e1a)
