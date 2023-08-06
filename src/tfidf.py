from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
import pandas as pd
import pickle
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


class TFIDF():
    def __init__(self, corpus) -> None:
        self.tfidfvectorizer = TfidfVectorizer(ngram_range=(1,2),
                                               tokenizer=self._tokenizer,
                                               min_df=3)
        # Train model
        self.tfidf_matrix = self.tfidfvectorizer.fit_transform(corpus)
        
    def _tokenizer(self, s):
        stemmer = SnowballStemmer('spanish')
        lemmatizer = WordNetLemmatizer()
        s = nltk.word_tokenize(s)
        stop_words = set(stopwords.words('spanish'))
        s = [token.lower() for token in s if token.lower() not in stop_words]
        s = [stemmer.stem(item) for item in s]
        # No es muy recomendable utilizar el lemmatizer, pero faltan más pruebas.
        s = [lemmatizer.lemmatize(token) for token in s]
        return s
    
    def query_documents(self, query:str, n_documents=10) -> dict:
        """
        Dada una query en formato de texto devuelve los n_documents más relevantes.
        """
        vector_query = self.tfidfvectorizer.transform([query])
        similarities = cosine_similarity(vector_query, self.tfidf_matrix)

        indices_most_similar = similarities.argsort()[0][-n_documents:][::-1]
        
        # Obtener los valores de similitud correspondientes
        most_similar_values = similarities[0, indices_most_similar]
        # Crear el diccionario con los índices y valores de similitud
        similarities_dict = {}
        for i, index in enumerate(indices_most_similar):
            similarity_value = most_similar_values[i]
            similarities_dict[index] = similarity_value
        return similarities_dict
    
    def get_vocabulary(self) -> dict:
        """
        Devuelve el vocabulario encontrado por el modelo.
        """
        return self.tfidfvectorizer.vocabulary_
    
    def get_stop_words(self):
        """
        Devuelve stop words para realizar analisis. Estas palabras no aportan nada al modelo.
        """
        try:
            stop_words = self.tfidfvectorizer.stop_words_
            return stop_words
        except:
            print("Fueron eliminadas las stop words")
        return None
        
    
    def delete_stop_words(self) -> None:
        """
        Eliminar atributo 'stop_words_'. Sirve para optimizar el modelo y que no ocupe mucho espacio.
        """
        delattr(self.tfidfvectorizer, "stop_words_")
        return None
    
    
    

def realizar_consultas(query:str):
    indices = model.query_documents(query)
    urls = df["metadata"].apply(lambda x: x.get("url"))
    print("\nConsulta 1:", query)
    print("Respuestas:\n")
    print("Indices:\n")
    print(indices)
    documents_most_similar = [urls[idx] for idx in indices]
    print("Documentos:\n")
    print(documents_most_similar)
    
if __name__ == "__main__":
    df = pd.read_json('data/textos_2023_08_0111_50_30.json')
    corpus = np.array(df["document"])
    model = TFIDF(corpus)
    

    query = "Cuál es el plan de estudios de la licenciatura en física"
    realizar_consultas(query)
    
    query = "Cómo cambiar de carrera?"
    realizar_consultas(query)    
    
    query = "\n\nQué es CELEX?"
    realizar_consultas(query)
    
    query = "\n\nDonde esta el edificio H"
    realizar_consultas(query)
    
    query = "\n\nQuién es el rector de la UAMI"
    realizar_consultas(query)
    
    
    
    model.delete_stop_words()    
    with open("models/model_2023_08_0111_50_30_4.pickle", "wb") as f:
        pickle.dump(model, f)
