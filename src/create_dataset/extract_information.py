import requests
import io
# import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from nltk.probability import FreqDist
from urllib.parse import urlparse


# nltk.download('punkt')
# nltk.download('stopwords')



class Extract_text_keywords():
    """
    Extrae palabras clave y vector en base a una url.
    
    :params: Una url
    :return: Texto extraido y palabras clave
    """
    
    def __init__(self, url, cantidad_keywords=20, min_length_keywords=3) -> None:
        self.url = url
        self.cantidad_keywords = cantidad_keywords
        self.min_length_keywords = min_length_keywords
    
    def is_internal_link(self, base_url, link):
        # Función para verificar si un enlace es interno (pertenece al mismo dominio) o externo.
        return urlparse(link).netloc == urlparse(base_url).netloc
    
    def clean_text(self, text):
        # Eliminar saltos de línea excesivos (más de dos seguidos) y saltos de línea separados por espacios
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        
        # Eliminar exceso de espacios vacíos y sustituir por un solo salto de línea
        text = re.sub(r'\s{2,}', '\n', text)
        
        # Eliminar espacios en blanco al comienzo o final de cada línea
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        
        # Unir las líneas limpias en un solo texto
        cleaned_text = '\n'.join(lines)
        
        return cleaned_text
        

    def scraping_text(self) -> str:
        txt = ""
        try:
            response = requests.get(self.url)
        except:
            raise Exception("Hubo un error con la:"+str(self.url))
        if self.url.endswith('.pdf'):
            f = io.BytesIO(response.content)
            reader = PdfReader(f)
            for page in reader.pages:
                txt += page.extract_text()
        else:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # Filtrar los enlaces externos y los scripts
            for element in soup.find_all(['a', 'script']):
                if element.name == 'a' and element.has_attr('href') and not self.is_internal_link(self.url, element['href']):
                    element.extract()  # Eliminar el enlace externo
                elif element.name == 'script':
                    element.extract()  # Eliminar los scripts
            # Extraer el título de la página (que aparece en las pestañas del navegador)
            txt = soup.title.string.strip()
            # Extraer el texto completo
            txt += soup.text
            txt = self.clean_text(txt)
            # txt = txt.replace('\n', ' ')
        return txt
    
    
    def preprocess_text(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        
        stop_words = set(stopwords.words('spanish'))
        filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and len(token) >= self.min_length_keywords]
        
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
        
        return stemmed_tokens


    def get_main_keywords(self, tokens):
        freq_dist = FreqDist(tokens)
        main_keywords = freq_dist.most_common(self.cantidad_keywords)
        return main_keywords
    
    
    def keywords_to_array(self, keywords):
        keywords_list = [kw[0] for kw in keywords]
        keywords_string = ", ".join(keywords_list)
        return keywords_string
    
    
    def run(self):
        text = self.scraping_text()
        preprocessed_text = self.preprocess_text(text)
        main_keywords = self.get_main_keywords(preprocessed_text)
        keywords_arr = self.keywords_to_array(main_keywords)
        # vector = self.vectorize_document(text)
        return text, keywords_arr






# urls = [# "https://www.celex.izt.uam.mx/instructivocelex.pdf",
#         "https://pcyti.izt.uam.mx/?page_id=3831",
#         "http://www.izt.uam.mx/index.php/historia/"]
# # urls = "https://www.celex.izt.uam.mx/instructivocelex.pdf"

# extractor = Extract_information(urls[0])
# texto, keywords = extractor.run()

# print(f"{texto} \n\n\n{keywords}")