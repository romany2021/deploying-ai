"""
Chatbot service tools:
  Service 1 - get_weather from Open-Meteo public API
  Service 2 - semantic search for search_kitchen_wisdom over persistent ChromaDB
  Service 3 - recipe math calculator as a function-calling tool
Completion: DONE
"""

import ast
import operator
import requests
import config
from vectorstore import get_collection

# Service 1 - get_weather from Open-Meteo public API. Miso rephrases these, never verbatim.
def get_weather(city: str) -> str:

    # geocode: turn the city NAME into latitude/longitude.
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=10,
    ).json()
    if not geo.get("results"):
        return f"No location found for '{city}'."
    place = geo["results"][0]
    lat, lon = place["latitude"], place["longitude"]

    # get current weather for coordinates.
    wx = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        timeout=10,
    ).json()
    cur = wx.get("current_weather", {})

    # Return facts about the place and its current weather and rephrase it.
    return (
        f"{place['name']}, {place.get('country', '')}: "
        f"temperature {cur.get('temperature')} C, wind {cur.get('windspeed')} km/h."
    )

# Service 2 - semantic search for search_kitchen_wisdom over persistent ChromaDB
def search_kitchen_wisdom(query: str, k: int = 3) -> str:
    collection = get_collection()
    res = collection.query(query_texts=[query], n_results=k)
    docs = res["documents"][0]
    cats = [m["category"] for m in res["metadatas"][0]]
    if not docs:
        return "No matching kitchen wisdom found."
    return "\n".join(f"- ({c}) {d}" for c, d in zip(cats, docs))

# Service 3 - recipe math calculator as a function-calling tool
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.Mod: operator.mod, ast.USub: operator.neg,}

# Walk a parsed expression tree and compute its value (only math, nothing else)
def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")

# Evaluate basic arithmetic like '250 * 3' without Python's unsafe eval()
def calculate(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode="eval").body
        result = _safe_eval(tree)
        return str(result)
    except Exception:
        return f"Could not compute '{expression}'."
