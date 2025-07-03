import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configure Gemini ---
genai.configure(api_key="AIzaSyAbyk4r2SfZJelOq2u2DL1ll87kF2Dteag")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Text to speech ---
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- Speech recognition ---
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        return query
    except Exception as e:
        print(f'Error: {e}')
        return 'None'

# --- Gemini response generator ---
def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text.replace("*", "")

# --- Telegram bot handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Jarvis. Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("Processing your request...")
    response = generate_response(user_msg)
    await update.message.reply_text(response)

# --- Telegram bot runner ---
def run_telegram_bot():
    application = ApplicationBuilder().token("7616675073:AAGoV2rIXkaBDyzCK2P5X50VPnZZpPqMbuU").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram bot is running...")
    application.run_polling()

# --- Main menu ---
if name == "main":
    print("Choose mode:")
    print("1. Voice Assistant")
    print("2. Telegram Bot")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        speak("Hello, I am Jarvis. How can I help you today?")
        while True:
            user_input = takeCommand()
            if user_input.lower() == "exit":
                speak("Goodbye!")
                break
            print(f"User: {user_input}")
            print("Processing...")
            reply = generate_response(user_input)
            print(f"Jarvis: {reply}")
            speak(reply)

    elif choice == "2":
        run_telegram_bot()
    else:
        print("Invalid choice.")
