import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string
import os
from langchain_community.document_loaders import YoutubeLoader

# Carga el video
loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=UNlJp4KrHoA&t=496s", 
                                        add_video_info=True, language=["es"])
transcripcion = loader.load()

details = (
    f"Video de: {transcripcion[0].metadata['author']} "
    f"con un tamaño de {transcripcion[0].metadata['length']} segundos\n"
    f"Título: {transcripcion[0].metadata['title']}\n\n"
    f"{transcripcion[0].page_content}"
)


nltk.download('punkt')
nltk.download('stopwords')

def resumen_hibrido(texto, num_oraciones=5):
    stop_words = set(stopwords.words('spanish'))
    oraciones = sent_tokenize(texto)
    frecuencia_palabras = Counter([palabra for palabra in word_tokenize(texto.lower()) if palabra not in stop_words and palabra not in string.punctuation])
    
    # Puntuación de las oraciones según la frecuencia de palabras
    puntuacion_oraciones = {oracion: sum(frecuencia_palabras.get(palabra, 0) for palabra in word_tokenize(oracion.lower())) for oracion in oraciones}
    oraciones_clasificadas = sorted(puntuacion_oraciones, key=puntuacion_oraciones.get, reverse=True)
    
    # Selección heurística: primeras oraciones de párrafos
    parrafos = texto.split('\n')
    oraciones_heuristicas = [sent_tokenize(parrafo)[0] for parrafo in parrafos if sent_tokenize(parrafo)]
    
    # Filtrar oraciones heurísticas que no están en la lista original
    oraciones_heuristicas = [oracion for oracion in oraciones_heuristicas if oracion in oraciones]
    
    # Combinación de oraciones seleccionadas y heurísticas
    oraciones_combinadas = sorted(set(oraciones_clasificadas[:num_oraciones] + oraciones_heuristicas), key=lambda s: oraciones.index(s))
    
    # Limitar el resumen final a 500 caracteres
    resumen_final = " ".join(oraciones_combinadas)[:2000]
    
    return resumen_final

texto = details
resumen = resumen_hibrido(texto, 5)
os.system('cls')
print(resumen)
