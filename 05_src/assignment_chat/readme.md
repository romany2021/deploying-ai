# The Byte Bistro — Chat with Miso

A chat assistant with a personality: **Miso**, the digital chef of a diner called
The Byte Bistro. Miso is friendly and talks about food. The chat is built with
Gradio, and the model uses function calling to decide which service to run.

## Services

1. **get_weather (API)** — gets a city's current weather from the free Open-Meteo
   API. Miso rephrases the result instead of showing the raw data.
2. **search_kitchen_wisdom (semantic search)** — searches a small knowledge base
   of cooking tips stored in a persistent ChromaDB collection.
3. **calculate (function calling)** — does basic arithmetic, useful for scaling
   recipes.

## Chat interface

- Built with Gradio (`ChatInterface`).
- Keeps memory during the conversation by passing the history back each turn.
- Long conversations are trimmed to the last few messages so they don't get too
  big (`MAX_HISTORY` in `chatbot.py`).

## Guardrails

- Refuses to reveal or change its system prompt.
- Won't talk about cats/dogs, horoscopes/zodiac signs, or Taylor Swift.

These are checked in `guardrails.py` before the model is called, and the rules are
also repeated in the system prompt.

## Knowledge base / embeddings

The knowledge base is `data/knowledge.csv`. `build_index.py` reads it and embeds
the text with `text-embedding-3-small` into a persistent ChromaDB store
(`chroma_store/`), which is included in the repo. You don't need to re-run it.

## How to run

```bash
cd 05_src/assignment_chat
python build_index.py   # only needed if chroma_store/ is missing
python app.py
```

Uses the course environment and the `.env` / `.secrets` files in `05_src/`.

## Notes

- I used function calling as the single way to route between services instead of
  building a separate router.
- The guardrails use simple keyword checks, which could be improved later with an
  LLM-based check.
