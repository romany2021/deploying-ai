"""
config file to load environment variables instead of hardcoding them. Used by the assignment_chat module and its tests.
Completion: DONE
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Absolute path to .../05_src/assignment_chat
HERE = Path(__file__).resolve().parent
SRC_DIR = HERE.parent

sys.path.append(str(SRC_DIR))

load_dotenv(SRC_DIR / ".env")
load_dotenv(SRC_DIR / ".secrets")

# Chat model & Embedding model
MODEL = os.getenv("MODEL", "gpt-4o-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

# AWS API Gateway proxy.
GATEWAY_BASE_URL = os.getenv(
    "API_GATEWAY_URL",
    "https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
)
GATEWAY_KEY = os.getenv("API_GATEWAY_KEY")

# Chroma
CHROMA_PATH = str(HERE / "chroma_store")
COLLECTION_NAME = "byte_bistro_kb"
KB_CSV = HERE / "data" / "knowledge.csv"
