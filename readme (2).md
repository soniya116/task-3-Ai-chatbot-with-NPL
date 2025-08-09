# 🤖 Smart NLP Chatbot

An intelligent chatbot that integrates Natural Language Processing (NLP), web search, and summarization using OpenAI’s GPT model. Built using Streamlit with a Telegram-like user interface.

---

## 🚀 Features

- 🔎 **Wikipedia & DuckDuckGo Search** for factual and general questions
- 🧠 **NLP Keyword Extraction** using spaCy
- ✨ **LLM-based Summarization** (OpenAI GPT)
- 💬 **Chat UI** using Streamlit


---
---bash

pip install -r requirements.txt
python -m spacy download en_core_web_sm
---
streamlit run app.py
Double click to view the replies by bot.