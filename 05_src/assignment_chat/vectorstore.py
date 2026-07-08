"""
Opens the persistent ChromaDB collection used for semantic search.
Linked to build_index.py (write side) and services.py (read side),
so the embedding configuration lives in one place and can never drift apart.
Completion: DONE
"""

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import config 
 
def _embedding_function():
    return OpenAIEmbeddingFunction(
        model_name=config.EMBED_MODEL,
        api_key="any value",
        api_base=config.GATEWAY_BASE_URL,
        default_headers={"x-api-key": config.GATEWAY_KEY},
    )

# PersistentClient writes to disk, so the index survives restarts  
def get_collection():
    client = chromadb.PersistentClient(path=config.CHROMA_PATH)
    return client.get_or_create_collection(
        name=config.COLLECTION_NAME,
        embedding_function=_embedding_function(),
    )