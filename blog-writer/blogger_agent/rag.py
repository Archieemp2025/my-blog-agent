import os
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

# Load env from blogger_agent/.env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Cache the index after first build
_rag_index = None


def _get_embedding_model() -> OpenAIEmbedding:
    """Return the configured OpenAI embedding model."""
    model_name = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    return OpenAIEmbedding(model=model_name)


def _build_rag_index():
    """Build an in-memory vector index from files in internal-data/."""
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "internal-data"

    if not data_dir.exists():
        return None

    files = list(data_dir.glob("*"))
    if not files:
        return None

    documents = SimpleDirectoryReader(str(data_dir)).load_data()

    Settings.embed_model = _get_embedding_model()
    Settings.node_parser = SimpleNodeParser.from_defaults(
        chunk_size=256,
        chunk_overlap=20,
    )

    return VectorStoreIndex.from_documents(documents)


def _get_rag_index():
    """Lazy-load the RAG index."""
    global _rag_index

    if _rag_index is None:
        try:
            _rag_index = _build_rag_index()
        except Exception as e:
            print(f"RAG index build failed: {e}")
            _rag_index = None

    return _rag_index


def search_internal_data(query: str) -> str:
    """Search local internal documents and return relevant text chunks."""
    index = _get_rag_index()

    if index is None:
        return (
            "Internal knowledge base is not available. "
            "Make sure the internal-data folder exists and contains files."
        )

    try:
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)

        if not nodes:
            return f"No relevant internal documents found for query: {query}"

        results = []
        for i, node in enumerate(nodes, start=1):
            text = node.text.strip()
            results.append(f"[Result {i}]\n{text}")

        return "\n\n".join(results)

    except Exception as e:
        return f"Internal knowledge search failed: {e}"