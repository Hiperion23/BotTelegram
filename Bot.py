from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import telebot
import requests
import openai

# Crea un objeto bot con tu token
bot = telebot.TeleBot("")
openai.api_key = ''

# Configura las credenciales de IBM Watson Speech to Text
authenticator = IAMAuthenticator('')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

# Configura la URL de servicio de IBM Watson Speech to Text
speech_to_text.set_service_url('')


# Maneja el comando '/start'
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Hola! Soy un bot, Me llamo Sykomv.")

# Maneja mensajes de texto
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Respuestas condicionales
    if message.text.lower() == 'hola' or  message.text.lower() == 'adios':
        bot.reply_to(message, "Hola! ¿Cómo estás?" if message.text.lower() == 'hola' else "¡Hasta luego!") 
    else:
        # Si no es 'hola' ni 'adios', utiliza ChatGPT para generar una respuesta
        try:
            response = openai.Completion.create(
                engine="text-davinci-001",  # Reemplaza "gpt-3.5-turbo" con el modelo adecuado
                prompt=f"You are a helpful assistant. User: {message.text.lower()}",
                temperature=0.7,
                max_tokens=50,
                n=1,  # Indica la cantidad de respuestas a generar (aquí solo se necesita 1)
                stop=None,
                frequency_penalty=0,
                presence_penalty=0
            )
            bot.reply_to(message, response.choices[0].text.strip())  # Envía la respuesta de ChatGPT al usuario
        except Exception as e:
            print("Error al obtener la respuesta de ChatGPT:", e)
            bot.reply_to(message, "Lo siento, hubo un problema al procesar tu mensaje.")

# Maneja mensajes de voz
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    file_info = bot.get_file(message.voice.file_id)
    file_url = 'https://api.telegram.org/file/bot{}/{}'.format(bot.token, file_info.file_path)
    
    # Descarga el archivo de audio
    audio_file = requests.get(file_url)
    
    # Realiza la transcripción de voz utilizando IBM Watson Speech to Text
    with open('audio.ogg', 'wb') as f:
        f.write(audio_file.content)

    try:
        with open('audio.ogg', 'rb') as audio_file:
            response = speech_to_text.recognize(audio=audio_file, content_type='audio/ogg').get_result()

            # Obtén el texto transcritos
            text = response['results'][0]['alternatives'][0]['transcript']

            # Responde al usuario con el texto transcritos
            bot.reply_to(message, f"Transcripción: {text}")
    except Exception as e:
        print("Error al transcribir el audio:", e)
        bot.reply_to(message, "Lo siento, no pude transcribir el audio.")

# Ejecuta el bot
bot.polling()
