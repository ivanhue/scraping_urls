import requests
import httpx
import asyncio
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
from bs4 import BeautifulSoup
import numpy as np
import pickle
import csv
import pandas as pd
import logging
from pprint import pprint

import cProfile, pstats
import os
import io
from datetime import datetime
fecha = datetime.today().strftime('%Y_%m_%d%H_%M_%S')

folder = "logs/"+fecha+"/"
if not os.path.exists(folder):
    os.makedirs(folder)



"""
TODO: 
    1. obligatorio que sean paginas de la UAM 
    2. añadir multithreading.
    3. poner un límite en el while.
    4. try except para detener manualmente.


"""

logging.basicConfig(filename=folder+'registro_errores_'+fecha+'.log', 
                    encoding='utf-8',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')
fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

obligatorios = ['http',
                'uam']

incluidos = ['.izt',
             'uami',
             'iztapalapa']


def generador_patrones():
    # Obligatorios
    cadena = r"^"
    for element in obligatorios:
        cadena += (r"(?=.*" + element + r")")
    
    # Opcionales
    cadena += r"(?=.*(?:"
    for element in incluidos:
        cadena += (element+r"|")
    return re.compile(cadena[:-1]+r"))")

def get_urls(soup, patron) -> set:
    urls = set()
    for link in soup.find_all('a', {'href': re.compile(patron)}):
        tmp = link.get('href')
        # if tmp[0] =='h':
        urls.add(tmp)
    # if len(urls)==0:
        # print("No encontro mas urls", patron)
    
    return list(urls)

def añadir_lista(lista1: list, lista2: list):
    for element in lista2:
        if not element in lista1:
            lista1.append(element)
    return lista1


def guardar_archivos(data):
    df = pd.DataFrame(data)
    df.to_csv(folder+"output"+fecha+".csv", index=False)
    df.to_pickle(folder+"output"+fecha+".pkl")
    # with open(folder+'urls'+fecha+'.pickle', 'wb') as handle:
    #     pickle.dump(todas_las_urls, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # np.savetxt(folder+"urls"+fecha+".csv", np.array(todas_las_urls,dtype=object), delimiter=",", fmt='%s')
    # open the file in the write mode
    # with open(folder+'urls'+fecha+'.csv', 'w', encoding='UTF8') as f:
    #     # create the csv writer
    #     writer = csv.writer(f)

    #     # write a row to the csv file
    #     writer.writerow(["Todos","Visitados","No_visitados"])
    #     writer.writerows(todas_las_urls)

async def fetch(urls):
    for url in urls:
        
    


def crear_dataset():
    patron = generador_patrones()
    url = 'https://pcyti.izt.uam.mx/?page_id=3831' # 'https://www.cseuami.org/'
    urls = [url, "http://www.iztapalapa.uam.mx/", "https://www.cseuami.org/"]
    urls_visited = []
    urls_no_visitadas = []
    count = 1
    
    
    while count<8_000:
        try:
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            urls_visited.append(url)
            urls = añadir_lista(urls, get_urls(soup, patron))
        except Exception as e:
            logging.error(" "+str(url)+ ' No pudo entrar: '+ str(e))
            urls_no_visitadas.append(url)
        try: 
            url = list(urls)[count]
        except:
            logging.error("Ya no hay más archivos")
            break
        count=count+1
        if count % 1_000 == 0:
            now = datetime.now()
            print(now.strftime("%H:%M:%S")+" | faltan: "+ str(len(urls) - count) + " links.")
            
    
    urls_visited += [''] * (len(urls) - len(urls_visited))
    urls_no_visitadas += [''] * (len(urls) - len(urls_no_visitadas))
    data = {"Todas":list(urls), "Visitadas":urls_visited, "No_visitadas":urls_no_visitadas}
    
    guardar_archivos(data)
    



if __name__ == "__main__":
    os.system('cls')
    profiler = cProfile.Profile()
    profiler.enable()
    
    crear_dataset()
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats(pstats.SortKey.CUMULATIVE)
    stats.strip_dirs()
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
    # ps.print_stats()
    stats.dump_stats(filename="profiling_"+fecha+".prof")
    with open(folder+'test_'+fecha+'.txt', 'w+') as f:
        f.write(s.getvalue())