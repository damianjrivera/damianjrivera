from pytube import YouTube
from moviepy.editor import *
import os

def descargar_audio_mp3(url, ruta_salida="jungle.mp3"):
    try:
        # link de video
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        
        # Descargar el archivo de audio
        archivo_descargado = video.download(filename="temp_video")
        
        # Convertir el archivo descargado a MP3
        clip = AudioFileClip(archivo_descargado)
        clip.write_audiofile(ruta_salida)
        clip.close()
        
        # Eliminar el archivo temporal de video
        os.remove(archivo_descargado)
        
        print(f"Audio descargado exitosamente como {ruta_salida}")
    except Exception as e:
        print("Ocurrió un error:", e)

url = input("Ingresa la URL del video de YouTube: ")
descargar_audio_mp3(url)
