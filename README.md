# Project Setup

## Installation

### Using Conda
If you have Conda installed, create the environment using the following command:
```sh
conda env create -f environment.yml
```
Then activate the environment:
```sh
conda activate <env_name>
```

### Using Pip
If you do not have Conda, install dependencies using:
```sh
pip install -r requirements.txt
```

## Running the Code
To run the project, execute:
```sh
python main.py -d 0
```

### Flags
The script accepts the following flags:
- `-d` for ERP demo
- `-i` for interview
- `-p` for payment follow-up
- `-o` for request for order placement

The integer following the flag specifies the index of the customer being talked to.

## Details About Models and Datasets Used
- **Language Model**: Mistral API via LangChain, used for handling conversations with prompt engineering.
- **Speech-to-Text (STT)**: Google Speech-to-Text API for transcribing user speech.
- **Text-to-Speech (TTS)**: Google Text-to-Speech API for converting responses into speech.
- **Calendar Integration**: Google Calendar API for scheduling ERP demos.
- **Data Handling**: Customer data is stored in structured JSON format to maintain consistency in responses.

## Agent Architecture and Key Components
- **State Management**: A Deterministic Finite Automaton (DFA) is used to manage different conversation scenarios, ensuring structured dialogue flow.
- **Prompt Engineering**: Custom prompts are designed for each state, enforcing structured responses.
- **Intent Recognition**: Handled by the LLM to determine the appropriate next state in the conversation.
- **Data Handling**: Scheduling and client data are passed using structured JSON to maintain clarity and prevent inconsistencies.

## Challenges and Solutions
1. **Ensuring Natural Conversation Flow**: This was addressed using a state-based approach where each scenario has a specific conversation flow.
2. **Handling Large Data Inputs**: Client and scheduling data were formatted into structured JSON and embedded within the prompts to ensure clarity and maintain consistency.

