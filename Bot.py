from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import telebot
import requests

# Crea un objeto bot con tu token
bot = telebot.TeleBot("6609925188:AAH7HTH5cGTa35GG90PORjpoV7OPIJB87T8")

# Configura las credenciales de IBM Watson Speech to Text
authenticator = IAMAuthenticator('CnxW9oIaYALaqdjlVLRXfflgIVi1cULZvFr-RM8HGtDj')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

# Configura la URL de servicio de IBM Watson Speech to Text
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/09628668-1d3e-49ba-ad65-d6da3de0048d')


# Maneja el comando '/start'
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Hola! Soy un bot de ejemplo.")

# Maneja mensajes de texto
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Respuestas condicionales
    if message.text.lower() == 'hola' and 'Hola' and 'ola' and 'Ola':
        bot.reply_to(message, "Hola! ¿Cómo estás?")
    elif message.text.lower() == 'adios':
        bot.reply_to(message, "¡Hasta luego!")
    else:
        bot.reply_to(message, "Lo siento, no entendí tu mensaje.")


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
