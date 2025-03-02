# Project Setup

## Installation

### Using Conda (Recommended)
If you have Conda installed, create the environment using:
```sh
conda env create -f environment.yml # Set the environment name and prefix in environment.yml
conda activate my_env  # Replace 'my_env' with the environment name.
```

### Using Pip
If Conda is not available, install dependencies using:
```sh
pip install -r requirements.txt
```

## API Key and Service Account Setup
You need to obtain API keys and set up authentication:

1. **Mistral API Key**: Get an API key from Mistral.
2. **Google Calendar API**:
   - Create a service account in Google Cloud.
   - Enable Google Calendar API.
   - Download the `service_account.json` file.
   - Place it in the project directory.
3. **Gmail Account**: Provide a Gmail account for calendar integration.

## Environment Variables (.env File)
Create a `.env` file in the project directory with the following content:
```
OPENAI_API_KEY=YOUR_MISTRAL_API_KEY
SCOPES=https://www.googleapis.com/auth/calendar
SERVICE_ACCOUNT_FILE=service_account.json
EMAIL_ID=YOUR_GMAIL_ID
```
Replace `YOUR_MISTRAL_API_KEY` and `YOUR_GMAIL_ID` with actual values.

## Running the Project
To run the project, use the following command:
```sh
python main.py -d 0
```

### Flags Explanation
There are four flags to specify the type of conversation:
- `-d` for ERP demo
- `-i` for interview
- `-p` for payment follow-up
- `-o` for order placement

The integer specifies the index of the customer being talked to.

## Agent Design Choices
- **LangChain with Mistral API**: Used for LLM-based conversation with prompt engineering.
- **State Management using DFA**: Ensures structured and natural conversation flow.
- **Speech-to-Text (STT) and Text-to-Speech (TTS)**: Google Speech-to-Text for input and Google Text-to-Speech for output.
- **Google Calendar Integration**: Used for scheduling ERP demo events.
- **Intent Recognition**: Handled by LLM for guiding conversation flow.

## Challenges and Solutions
- **Natural Conversation Flow**: Managed using state management (DFA) to keep responses structured per scenario.
- **Handling Data for Scheduling and Client Information**: Resolved through structured JSON responses enforced via prompt engineering.

## Model and Dataset Details
- The LLM used is Mistral API, fine-tuned via prompt engineering.
- Google Speech-to-Text and Google Text-to-Speech were used for audio processing.
- Google Calendar API manages ERP demo scheduling.

## Loom Video link
[Intro](https://www.loom.com/share/bb590f88f78040bb83d6ce182cc829af?sid=e1e4693d-0f48-43cf-8548-69a073ada110)
[Demo](https://www.loom.com/share/6ae86f39f80b48a68dd03591bbf71efc?sid=c4431adf-191c-4d0e-985a-657cff8b2c2a)

## Features Implementation Status
### Implemented:
- Conversation handling for all scenarios
- State management system
- Calendar event scheduling
- Intent recognition

### Not Implemented:
- Storing skills and experience gathered during interviews in a file
- Improved Hinglish Text-to-Speech quality

