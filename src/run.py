from create_dataset import web_crawler, update_data, FECHA, FOLDER
import asyncio
import os
import cProfile, pstats
import pickle
import json
import argparse
from tfidf import TFIDF
import pandas as pd
import numpy as np



def check_performance(function):
    """
    Sirve para checar el performance de una función y devuelve las estadísticas en un 
    archivo .profile.
    
    Ejemplo para analizar los resultados:
        >>> snakeviz file.profile
    """
    def performance():
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = function()
        
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats(pstats.SortKey.CUMULATIVE)
        stats.strip_dirs()
        stats.dump_stats(filename=FOLDER+"profiling_"+FECHA+".prof")
        return result
            
    return performance



@check_performance
def create_data_set():
    data = asyncio.run(web_crawler())
    docs, keywords, urls = data
    data_list = []
    
    # Generar la estructura de los datos que se guardarán:
    for doc, kw, url in zip(docs, keywords, urls):
        docdata = {}
        metadata = {}
        docdata["document"] = doc
        metadata["keywords"] = kw
        metadata["url"] = url
        docdata["metadata"] = metadata
        data_list.append(docdata)
        
    
    with(open("data/textos_"+FECHA+".json", "w")) as f:
        json.dump(data_list, f, indent=4)
    
    
    if not os.path.isfile(model_path):
        df = pd.read_json('data/textos_2023_08_0111_50_30.json')
        corpus = np.array(df["document"])
        model = TFIDF(corpus)
        
        model.delete_stop_words()    
        
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
    else:
        raise Exception("""El nombre del modelo contenido en la variable 'model_path' 
                        dentro del archivo 'run.py' ya existe, se debe cambiar el nombre
                        del modelo""")


def retriever(query:str):
    try:
        model = pickle.load(open(model_path, "rb"))
    except:
        raise Exception("No se tiene ningun modelo ya creado en:", model_path)
    results = model.query_documents(query)
    return results



def create():
    create_data_set()
    query = "Qué es celex?"
    docs = retriever(query)
    
    print("Pregunta: "+query)
    print("Respuesta: ",docs)

def update():
    asyncio.run(update_data())


if __name__ == "__main__":
    model_path = "models\model_2023_08_0111_50_30_7.pickle"
    
    parser = argparse.ArgumentParser(description='Crear / Actualizar base de datos.')
    parser.add_argument("-c", "--create", action="store_true", 
                        help="Crear nueva base de datos (INICIAL_PAGES)")
    parser.add_argument("-u", "--update", action="store_true", 
                        help="Actualizar base de datos (NUEVAS_PAGINAS)")
    
    args = parser.parse_args()
    
    if args.create:
        create()
    elif args.update:
        update()
    else:
        print("Debe seleccionar una función. Usa '-h' para obtener ayuda.")
    
    
    