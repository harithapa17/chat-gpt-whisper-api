import os
from dotenv import load_dotenv
import gradio as gr
import openai 
from pydub import AudioSegment
import datetime
from gtts import gTTS
from playsound import playsound

load_dotenv()                 
openai.api_key = os.getenv("OPENAI_API_KEY")

# user_id = input("Enter user ID: ")
# folder_name = user_id
user_id ="2"
 
 
folder_path = "audio_files/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
user_path = os.path.join(folder_path, user_id)  
if not os.path.exists(user_path):
    os.makedirs(user_path)

def translate(audio):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"{timestamp}.wav"
    i = 1
    while os.path.exists(file_name):
        file_name = f"{timestamp}_{i}.wav"
        i += 1

    file_path = os.path.join(user_path, file_name)
    audio = AudioSegment.from_file(audio, format="")
    audio.export(file_path, format="wav")
    file_path = open(file_path, "rb")
    transcript = openai.Audio.translate("whisper-1", file_path)
   
    response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": transcript["text"]},
                #   {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                #   {"role": "user", "content": "Where was it played?"}
                      ]
                  )
    
    text = response['choices'][0]['message']['content']
    speech = gTTS(text)
    speech_file_name = f"{timestamp}.mp3"
    speech_path = os.path.join(user_path, speech_file_name)
    speech.save(speech_path)
    playsound(speech_path)
    # return speech_path sd
ui = gr.Interface(fn=translate, inputs=gr.Audio(source="microphone", type="filepath"), outputs="audio", live=True)
ui.launch(share=True)
