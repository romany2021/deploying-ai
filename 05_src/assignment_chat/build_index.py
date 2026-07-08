"""
One-time script to build persistent Chroma index from the CSV.
Creates the ./chroma_store folder.
Completion: DONE
"""

import pandas as pd
import config
from vectorstore import get_collection

# Load the knowledge base from CSV
def main():
    df = pd.read_csv(config.KB_CSV)

    collection = get_collection()
    # prevent duplicate rerun
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # add the documents
    collection.add(
        ids=df["id"].astype(str).tolist(),
        documents=df["text"].tolist(),
        metadatas=[{"category": c} for c in df["category"]],
    )

    print(f"Indexed {len(df)} documents into '{config.COLLECTION_NAME}'.")

if __name__ == "__main__":
    main()