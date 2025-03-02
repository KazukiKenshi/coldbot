from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import re
import prompts
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime,timedelta
from dotenv import load_dotenv
from util import *



#######################################################################################################################################

#Load environment variables

load_dotenv()

max_retries = 3
current_datetime = datetime.now().strftime("%d-%m-%y %H:%M")
current_day = datetime.now().strftime("%A")

SCOPES = [os.getenv("SCOPES")]
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
EMAIL = os.getenv("EMAIL_ID")


pygame.mixer.init()
session_histories = {}
args = parse_arguments()
index = None
current_state = None

# parsing the command line argument and setting the initial state for conversation

if args.d is not None:
    current_state = "DEMO_INTRO"
    index = args.d
elif args.i is not None:
    current_state = "INTRODUCTION"
    index = args.i
elif args.p is not None:
    current_state = "PAYMENT_INTRO"
    index = args.p
elif args.o is not None:
    current_state = "ORDER_INTRO"
    index = args.o

os.environ["CURRENT_STATE"] = current_state or ""
os.environ["INDEX"] = str(index) if index is not None else ""

#######################################################################################################################################

# Function to load history to maintain context of conversation

def get_session_history(session_id):
    #Retrieve chat history for a given session.

    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()  
    return session_histories[session_id]


#######################################################################################################################################


llm = ChatOpenAI(model="mistral-large-2411", openai_api_base="https://api.mistral.ai/v1") # Instance of Mistral


recognizer = sr.Recognizer() #Instance of STT



#######################################################################################################################################



# Getting the first LLM response with an empty prompt
conversation = RunnableWithMessageHistory(
    runnable=ChatPromptTemplate.from_template(prompts.get_prompt(current_state)) | llm,
    get_session_history=get_session_history,
    input_key="user_input",
    history_key="history"
)

input_txt = ""  # Empty input for the first response

for attempt in range(max_retries):
    output_txt = conversation.invoke(
        {
            "user_input": input_txt
        },
        config={"configurable": {"session_id": "test"}}
    )

    response_text = output_txt.content
    print(f"Attempt {attempt + 1}: Raw Response:", response_text)
    
    clean_response = re.sub(r"```(?:json)?", "", response_text).strip()

    try:
        parsed_output = json.loads(clean_response)
        intent = parsed_output.get("intent", "UNKNOWN")
        reply = parsed_output.get("reply", "Sorry, I didn't understand that.")
        date = parsed_output.get("date", "UNKNOWN")
        next_question = parsed_output.get("next_question", "Unknown")
        skills = parsed_output.get("skills", "UNKNOWN")
        experience = parsed_output.get("experience", "UNKNOWN")
        break  # Exit loop if parsing is successful

    except json.JSONDecodeError:
        print(f"Attempt {attempt + 1}: JSON parsing failed. Retrying...")

else:
    print("Error from the LLM server side")
    intent, reply, date, next_question, skills, experience = "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"

# Play LLM's first response using TTS
print(reply)

with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
    temp_audio_path = temp_audio.name
    tts = gTTS(reply, lang="hi")
    tts.save(temp_audio_path)

pygame.mixer.init()
pygame.mixer.music.load(temp_audio_path)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    continue

current_state = get_next_state(current_state, intent)


#######################################################################################################################################


# Program Loop

with sr.Microphone() as source:
    print("Listening...")
    recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            # Getting user input
            print("Say something:")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            input_txt = recognizer.recognize_google(audio, language="en")

            print("You said:", input_txt)

            # Generating appropriate prompt for LLM

            prompt = ChatPromptTemplate.from_template(
                prompts.get_prompt(current_state)
            )

            conversation = RunnableWithMessageHistory(
                runnable=prompt | llm,
                get_session_history=get_session_history,
                input_key="user_input",
                history_key="history"
            )

            for attempt in range(max_retries):
                # Getting LLM response
                output_txt = conversation.invoke(
                    {
                        "user_input": input_txt
                    },
                    config={"configurable": {"session_id": "test"}}
                )

                response_text = output_txt.content
                print(f"Attempt {attempt + 1}: Raw Response:", response_text)
                
                clean_response = re.sub(r"```(?:json)?", "", response_text).strip()  # Cleaning response

                # Try parsing the response
                try:
                    parsed_output = json.loads(clean_response)
                    intent = parsed_output.get("intent", "UNKNOWN")
                    reply = parsed_output.get("reply", "Sorry, I didn't understand that.")
                    date = parsed_output.get("date", "UNKNOWN")
                    next_question = parsed_output.get("next_question", "Unknown")
                    skills = parsed_output.get("skills", "UNKNOWN")
                    experience = parsed_output.get("experience", "UNKNOWN")
                    
                    break  # Exit loop if parsing is successful

                except json.JSONDecodeError:
                    print(f"Attempt {attempt + 1}: JSON parsing failed. Retrying...")

            else:
                # If all attempts fail
                print("Error from the LLM server side")
                intent, reply, date, next_question, skills, experience = "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"
            next_state = get_next_state(current_state, intent) # Updating the next state for chatbot

            print(reply)
            print(f"Next State: {next_state}")

            # Scheduling event on Google Calendar

            if next_state == "SCHEDULE_DEMO":
            
                print(f"scheduling on {date}") 

                input_time = date
                parsed_time = datetime.strptime(input_time, "%Y-%m-%dT%H:%M:%S")
                start_time = parsed_time.strftime("%Y-%m-%dT%H:%M:%S")
                parsed_end_time = parsed_time + timedelta(hours=1)
                end_time = parsed_end_time.strftime("%Y-%m-%dT%H:%M:%S")


                schedule_demo(
                    "ERP demo schedule",
                    start_time,
                    end_time,
                    EMAIL,
                    SERVICE_ACCOUNT_FILE,
                    SCOPES
                )

            
            current_state = next_state

            # Saving a temporary audio file for TTS

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio_path = temp_audio.name
                tts = gTTS(reply, lang="hi")
                tts.save(temp_audio_path)

            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()
            
            # Playing the audio file

            while pygame.mixer.music.get_busy():
                continue
            
            # Stopping if the conversation reached to an end

            if current_state in ["END_DEMO","END_INTERVIEW","END_PAYMENT"]:
                print("Stopping...")
                break

        except sr.UnknownValueError:
            print("Couldn't understand, try again.")
        except sr.RequestError:
            print("Could not connect to the recognition service.")

print("Speech recognition loop ended.")