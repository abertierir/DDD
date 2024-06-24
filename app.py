import streamlit as st
import instaloader
import os
from moviepy.editor import VideoFileClip
from openai import OpenAI


st.title("Instagram Recipes")

#Form
with st.form(key='url_form'):
   
    url = st.text_input("Insert instagram video URL:")
    submit_button = st.form_submit_button(label='Download Transcription')

if submit_button:
    if url:
        try:
            # Crear una instancia de Instaloader
            L = instaloader.Instaloader()

            # Descargar el video y obtener metadatos
            post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
            L.download_post(post, target='downloads')

            # Mostrar el mensaje de éxito
            st.success("Video descargado exitosamente.")

            # Obtener la descripción del video
            description = post.caption
            st.write("Descripción del video:")
            st.write(description)

            # Obtener la ruta del video descargado
            video_path = None
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    video_path = os.path.join("downloads", file)
                    break

            if video_path:
                # Extraer el audio del video
                video = VideoFileClip(video_path)
                audio_path = "downloads/audio.mp3"
                video.audio.write_audiofile(audio_path)

                # Mostrar el audio extraído
                st.audio(audio_path)


        except Exception as e:
            st.error(f"Error al descargar o procesar el video: {e}")

    else:
        st.error("Por favor, ingresa una URL válida.")

    #Form to 
    
with st.form(key='transcription_form'):

    transcription_button = st.form_submit_button(label='Get Transcription')

if transcription_button:
    try:

        client = OpenAI()
                
        audio_file= open(audio_path, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
                
        st.subheader("Audio Transcription")
        st.write(transcription.text)

                # Eliminar los archivos después de mostrarlos
        os.remove(video_path)
        os.remove(audio_path)

    except Exception as e:
        st.error(f"Error al transcribir audio: {e}")