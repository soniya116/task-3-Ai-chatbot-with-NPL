import spacy
import wikipedia
from duckduckgo_search import DDGS
import openai
from config import OPENAI_API_KEY

nlp = spacy.load("en_core_web_sm")

# Setup OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def extract_keywords(text):
    doc = nlp(text)
    return " ".join([token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]) or text

def classify_intent(text):
    lowered = text.lower()
    if any(word in lowered for word in ["hi", "hello", "hey", "good morning", "good evening"]):
        return "greeting"
    if "how are you" in lowered:
        return "wellbeing"
    if any(q in lowered for q in ["who", "what", "where", "when", "define", "meaning", "explain"]):
        return "factual"
    if "how" in lowered:
        return "instructional"
    return "general"

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"(Wikipedia)\n{summary}"
    except Exception:
        return None

def search_duckduckgo_raw(query, max_results=3):
    """Returns raw text + urls for summarization."""
    results = []
    with DDGS() as ddgs:
        for res in ddgs.text(query, max_results=max_results):
            results.append({"title": res["title"], "body": res["body"], "url": res["href"]})
    return results

def summarize_with_llm(text):
    try:
        if not OPENAI_API_KEY:
            return text
        prompt = f"Summarize the following information in 2 concise sentences:\n\n{text}"
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.5
        )
        return res["choices"][0]["message"]["content"].strip()
    except Exception:
        return text

def get_response(user_input, rewrite_enabled=True):
    intent = classify_intent(user_input)

    if intent == "greeting":
        return "👋 Hello! How can I help you today?"
    elif intent == "wellbeing":
        return "I'm doing great, thanks! 😊 What would you like to know?"

    query = extract_keywords(user_input)

    # Try Wikipedia first
    if intent in ["factual", "instructional"]:
        wiki = search_wikipedia(query)
        if wiki:
            return wiki

    # Fallback to DuckDuckGo + summarize
    results = search_duckduckgo_raw(query)
    combined_text = "\n\n".join([r["body"] for r in results if r["body"]])
    summary = summarize_with_llm(combined_text)

    links = "\n".join([f"- [{r['title']}]({r['url']})" for r in results])
    return f"{summary}\n\n🔗 Useful Links:\n{links}" if summary else "Sorry, couldn't summarize that well."
