import json
import pandas as pd
import validators
import asyncio
import httpx
import re


from typing import List, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from .extract_information import Extract_text_keywords

import logging
from .constants import *

fecha = FECHA
folder = FOLDER
obligatorios = OBLIGATORIOS
incluidos = INCLUIDODS
excluidos = EXCLUIDOS



logging.basicConfig(filename=folder+'registro_errores_'+fecha+'.log', 
                    encoding='utf-8',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w',
                    level=logging.INFO)


def _generador_patrones():
    # Obligatorios
    cadena = r"^"
    for element in obligatorios:
        cadena += (r"(?=.*" + element + r")")
        
    # Exclusión
    for element in excluidos:
        cadena += (r"(?!.*" + element + r")")
    
    # Opcionales
    cadena += r"(?=.*(?:"
    for element in incluidos:
        cadena += (element+r"|")
    return re.compile(cadena[:-1]+r")).*$")


async def _get_urls(soup: BeautifulSoup, base_url: str) -> set[str]:
    """
    Método asincronico para obtener urls.
    
    :params: Objeto BeautifulSoup y url sobre la que se va hacer la consulta.
    :return: urls obtenidas de la pagina base.
    """
    urls = set()
    tmp_patron = _generador_patrones()
    pattern = re.compile(tmp_patron)
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        parsed_href = urlparse(href)
        # Verificar si el enlace es relativo
        if not parsed_href.netloc: 
            url = urljoin(base_url, href)
        else:
            url = href
        if bool(pattern.match(url)) and validators.url(url) and not url.endswith('.jpg') and not url.endswith('.png') and not url.endswith('.jpeg'):
            urls.add(url)
    return urls


async def _fetch(urls: List[str]) -> Tuple[List[BeautifulSoup], List[List[str]], List[str], List[str], List[str]]:
    # Configurar los tiempos de espera
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=500)
    timeout = httpx.Timeout(timeout=5.0, connect=5, read=10)  # Tiempo máximo de espera para conexión y lectura
    
    
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        tasks = []

        tasks = (client.get(url) for url in urls)

        reqs = await asyncio.gather(*tasks, return_exceptions=True)
        
    soups = []
    texts = []
    keywords_list = []
    unvisited = []
    visited = []
    for url, req in zip(urls, reqs):
        try:
            req.raise_for_status()
            soup = BeautifulSoup(req, 'html.parser')
            soups.append(soup)
            extractor = Extract_text_keywords(url)
            text, keywords = extractor.run()
            if not text or not keywords or len(text) < MIN_CANTIDAD_TEXTO:
                soups.pop()
                raise Exception("No hay texto en el documento.")
            if len(text) > MAX_CANTIDAD_TEXTO:
                soups.pop()
                raise Exception("Demasiado texto. Documento inválido.")
            keywords_list.append(keywords)
            texts.append(text)
            visited.append(url)
        except Exception as e:
            unvisited.append(url)
            logging.error(f"No pudo entrar {url} {str(e)[:80]}")
    return soups, keywords_list, unvisited, visited, texts



async def web_crawler():
    # Variables de tipo set para asegurar que los links visitados sean únicos.
    all_urls_set = set(INICIAL_PAGES)  # Almacena todas las paginas, visitadas o no visitadas.
    unvisited_set = set()              # Almacena paginas sin visitar.
    new_urls = all_urls_set            # ALmacena paginas que van a ser visitadas.
    
    # Variables para detenerse
    count = len(new_urls)              # Cuenta las paginas que se intentaron visitar.
    finished = False                   # Checa si ya no hay más paginas por visitar.
    max_pages_visited = False          # Checa si se visito la máxima cantidad de paginas propuestas (MAX_PAGES).
    
    # Variables en orden utilizadas para guardar en BD. Se asegura que sean únicas ya que 
    keywords_list = []                 # Almacena palabras clave que serán guardadas en BD.
    visited_list = []                  # Almacena paginas visitadas que serán guardadas en BD.
    text_list = []                     # Almacena el texto de las paginas, este no sera guardado en la BD.
    
    imprimir = 0
    while not finished and not max_pages_visited:
        # Se obtienen datos de las urls unicas. Por lo tanto, no se repiten los datos y se pueden actualizar para la BD.
        task_fetch = asyncio.create_task(_fetch(new_urls))
        responses = await task_fetch
        soups_response, keywords_response, unvisited_response, visited_response, texts_response = responses

        # Se agregan las keywords y urls de las páginas que sí se pudieron visitar.    
        text_list.extend(texts_response)
        keywords_list.extend(keywords_response)
        visited_list.extend(visited_response)
        
        # Se mantiene el registro de las páginas visitadas y no visitadas.
        unvisited_set.update(unvisited_response)

        # Se obtienen nuevas páginas web que no se sabe si ya fueron visitadas o no, por lo que aquí se debe usar estrictamente el tipo de dato set.
        results_list = (await asyncio.gather(*map(_get_urls, soups_response, visited_response)))

        
        # Se añaden las nuevas paginas descubiertas para visitarlas
        check_urls_set = set()
        for urls_scrapped in results_list:
            check_urls_set.update(urls_scrapped)
        
        # Filtrar paginas web obtenidas y guardar solo las no visitadas aún.
        new_urls = set()
        new_urls = check_urls_set - all_urls_set
        
        # Actualizar todas las paginas web a consultar.
        all_urls_set.update(new_urls)
        
        # Contar las nuevas paginas por visitar.
        count += len(new_urls) #  + len(unvisited_response)
        
        # Checar si terminó
        finished = (len(new_urls) == 0)
        
        # Checar si se excedió la maxima cantidad de paginas.
        max_pages_visited = MAX_PAGES < count
        
        imprimir += 1
        if imprimir % 1_000:
            print("###################################################################")
            print(f"Cantidad de páginas visitadas: {len(visited_list)}")
            print(f"Cantidad total de paginas: {len(all_urls_set)}")
            print(f"Faltan: {MAX_PAGES-count} paginas.")
            print(f"Cantidad que se van a visitar: {len(new_urls)}")
            print(f"Terminó: {finished}")
            print(f"Faltan más páginas: {max_pages_visited}")
            print()
        
        
    if max_pages_visited:
        logging.info("Terminó por maximas paginas visitadas")
    if finished:
        logging.info("Terminó por no poder encontrar más paginas") 
    return text_list, keywords_list, visited_list




async def update_data():
    path_data = BASE_DE_DATOS
    df = pd.read_json(path_data)
    urls = df["metadata"].apply(lambda x: x.get("url"))
    # keywords = df["metadata"].apply(lambda x: x.get("keywords"))
    # patron = re.compile()
    # if "https://www.cseuami.org/index.php/cambio-carrera" in df["metadata"].apply(lambda x: x.get("url")):
    # search_url = "https://cbi.izt.uam.mx/coddaa/index.php/fisica-pe"
    add_urls = []
    for new_url in NUEVAS_PAGINAS:
            # Checar si no existe el nuevo url.
        if not new_url in urls.values:
            
        # index = [i for i, x in enumerate((urls.values==new_url)) if x][0]
            print()
            add_urls.append(new_url)
        else:
            # TODO: Implementar el caso donde se actualiza una url existente.
            print("Sí existe esa pagina web en los datos.", new_url)
    task_fetch = asyncio.create_task(_fetch(add_urls))
    responses = await task_fetch
    _, keywords_list, __, visited, texts = responses
    
    data_list = []
    for doc, kw, url in zip(texts, keywords_list, visited):
        docdata = {}
        metadata = {}
        docdata["document"] = doc
        metadata["keywords"] = kw
        metadata["url"] = url
        docdata["metadata"] = metadata
        data_list.append(docdata)
    
    
    # 1. Read file contents
    with open(path_data, "r") as file:
        data = json.load(file)
    # 2. Update json object
    data.extend(data_list)
    # 3. Write json file
    with open(path_data, "w") as file:
        json.dump(data, file, indent=4)


# @_check_performance
def test():
    
    data = asyncio.run(web_crawler())
    print(len(data))
    # print("Test web crawler")
    # task_web_crawler = asyncio.create_task(web_crawler())
    # data = await task_web_crawler
    # print(len(data))
    return data


if __name__ == "__main__":
    # print("Test web_crawler")
    # paginas = ["https://www.celex.izt.uam.mx/instructivocelex.pdf",
    #         "http://books.toefsefscrape.com/catalogue/page-2.html",
    #         "http://books.toscrape.com/catalogue/page-2.html",
    #         "http://books.toscrape.com/catalogue/page-3.html",
    #         "http://books.toscrape.com/catalogue/page-4.html"]

    # asyncio.run(update_data())
    # test()
    # asyncio.run(test())
    
    ...