import chromadb
from typing import List



class Vectordb():
    """
    Base de datos vectorizada. Permite crear, añadir, eliminar o actualizar elementos.
    Al ser vectorizada permite mejorar las consultas y cambios con los vectores que en este caso representan
    documentos.
    
    Fuentes: https://docs.trychroma.com/
    """
    def __init__(self, path:str="data", name:str="paginas_uami") -> None:
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=name)
        return None
    
    
    def add(self, embeddings:List[List[float]], metadatas:List[dict], ids:List[str]) -> None:
        """
        Añade elementos a la base de datos.
        :params:
            ids: Recibe una lista de ids para identificar los elementos de la base de datos. Opcional.
            embeddings: Recibre una Lista de vectores que representan los documentos.
            metadata: Recibe una lista de datos adicionales como palabras clave, fecha de consulta y dirección.
        """
        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        return None
        
    
    def query(self, query_embeddings:List[List[float]], keywords,  n_results=5) -> List:
        """
        Hace consultas a la base de datos.
        :params:
            query_embeddings: Recibe una lista de vectores que se usan para consultar la base de datos.
            n_results: La cantidad de resutlados esperados, por defecto 5. 
        """
        result = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where={"keywords": keywords}
        )
        return result
        
        
    def update(self, ids:List[str]=[], embeddings:List[List[float]]=None, metadatas:List[dict]=None) -> None:
        """
        Actualiza la base de datos.
        :params:
            ids: Lista de identificadores. Opcional.
            embeddings: Lista de vectores. Opcional.
            metadatas: Lista de diccionarios con valores adicionales. Opcional.
        """
    
        self.collection.update(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )
        return None
    
    
    def delete(self, where:dict=None, ids:List[str]=None) -> None:
        """
        Elimina elementos de la base de datos.
        :params:
            where: Diccionario con condiciones a buscar. Opcional.
            ids: Identificadores a buscar. Opcional.
        """
        self.collection.delete(
            ids=ids,
            where=where
        )
        return None

if __name__ == "__main__":
    db = Vectordb()

    # db.add(embeddings=[[7.5,3.2],[3.5,2.8]],metadatas=[{"fecha":"hoy"},{"fecha":"ayer"}], ids=["1","2"])

    print(db.query(query_embeddings=[[7.6,3.1]],n_results=1))