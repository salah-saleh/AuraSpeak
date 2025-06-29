import os  # For accessing environment variables
import google.generativeai as genai  # For Gemini API
import json  # For parsing Gemini's JSON response
from utils.benchmark import benchmark_function  # For benchmarking

# Load Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)

# System prompt for Gemini
SYSTEM_PROMPT = """
You are an intent classifier and text polisher for a voice agent. Given a user utterance, return a JSON object with:
- intent: one of "web_search", "tts", or "clipboard"
- query: the relevant query or text for the intent, cleaned up and ready for use
- result_length: (for web_search) "short", "detailed", or "default" (inferred from the query or user instructions)

Instructions:
- For "web_search", extract the search query and infer the result length:
    - Use "short" for direct, factual, or time/date questions, or if the user asks for a brief answer.
    - Use "detailed" for broad, open-ended, or explanatory questions, or if the user asks for detail.
    - Use "default" if not specified or unclear.
- For "tts" and "clipboard", polish the text: remove filler words, pauses, and self-corrections. Only include what makes sense.
- If the user corrects themselves, only include the final intended message.

Examples:
User: what time is it in Paris?
{"intent": "web_search", "query": "current time in Paris", "result_length": "short"}

User: search the web for the politics of the USA
{"intent": "web_search", "query": "politics of the USA", "result_length": "detailed"}

User: search the web for the population of France, make it short
{"intent": "web_search", "query": "population of France", "result_length": "short"}

User: read this aloud, um, actually, say Hello world instead
{"intent": "tts", "query": "Hello world"}

User: This is a note, uh, wait, make that a reminder for tomorrow
{"intent": "clipboard", "query": "reminder for tomorrow"}
"""

@benchmark_function("gemini_intent_detection")
def detect_intent(text):
    """
    Uses Gemini to detect the user's intent and extract a cleaned-up query and result length.
    Returns a dict: {"intent": ..., "query": ..., "result_length": ...}
    """
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    prompt = SYSTEM_PROMPT + f"\nUser: {text}\n"
    response = model.generate_content(prompt)
    # Try to extract JSON from the response
    try:
        # Gemini may return text with code block formatting or extra text, so extract JSON
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        content = content.strip('`\n ')
        result = json.loads(content)
        # Ensure all expected keys are present
        intent = result.get("intent", "clipboard")
        query = result.get("query", text)
        result_length = result.get("result_length", "default")
        return {"intent": intent, "query": query, "result_length": result_length}
    except Exception as e:
        print(f"[Intent Detection Error] Could not parse Gemini response: {e}\nResponse: {getattr(response, 'text', response)}")
        # Fallback: treat as clipboard
        return {"intent": "clipboard", "query": text, "result_length": "default"} 