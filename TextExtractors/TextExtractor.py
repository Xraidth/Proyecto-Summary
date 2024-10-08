from langchain_community.document_loaders import YoutubeLoader
import os
import difflib

#Carga el video
loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=Oa9JkUyh3uU", 
                                        add_video_info=True, language = ["es"])
transcripcion = loader.load()

details = (
        f"Video de: {transcripcion[0].metadata['author']} "
        f"con un tamaño de {transcripcion[0].metadata['length']} segundos\n"
        f"Título: {transcripcion[0].metadata['title']}\n\n"
        f"{transcripcion[0].page_content}"
    )


os.system('cls')
print(details)







