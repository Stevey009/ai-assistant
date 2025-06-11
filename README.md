# ai-assistant

This project aims to build a private personal assistant inspired by JARVIS. It uses OpenAI's GPT-4 through a Streamlit interface and stores conversation history locally. The assistant supports journaling and simple feedback so that you can review past chats and rate responses.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key (one is already included with a placeholder):

```
OPENAI_API_KEY=your-api-key-here
```

3. Run the assistant:

```bash
streamlit run app.py
```

## Features

- **Streamlit Chat UI** – chat with GPT‑4 in your browser.
- **Persistent Memory** – conversation history is kept for the session.
- **Journaling** – each interaction is saved to `journal.json` with timestamps and feedback ratings.
- **Feedback Slider** – rate the assistant's responses to track quality over time.

Feel free to expand upon this foundation with additional capabilities like voice support or offline models.
