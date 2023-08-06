import pickle
from tfidf import TFIDF
import pandas as pd



datos_path = "data/textos_2023_08_0111_50_30.json"

df = pd.read_json(datos_path)
urls = df["metadata"].apply(lambda x: x.get("url"))
keywords = df["metadata"].apply(lambda x: x.get("keywords"))


with open('model_2023_08_0111_50_30_4.pickle', 'rb') as file: 
    model:TFIDF = pickle.load(file) 
    
    

def realizar_consultas(query:str):
    indices = model.query_documents(query)
    print("\nConsulta 1:", query)
    print("Respuestas:\n")
    print(indices)
    documents_most_similar = [urls[idx] for idx in indices]
    print(df["document"][list(indices.keys())[0]])
    print(documents_most_similar)
    
    
    

if __name__ == "__main__":
    
    query = "Qué es celex"
    results = model.query_documents(query)

    realizar_consultas(query)
