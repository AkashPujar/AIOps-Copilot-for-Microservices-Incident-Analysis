import os
from datetime import datetime

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


DATA_PATH = "data/"
VECTORSTORE_PATH = "vectorstore/"
RETRIEVAL_LOG_FILE = "logs/retrieval.log"


UNSUPPORTED_TERMS = [
    "kafka",
    "redis",
    "elasticsearch",
    "spark",
    "hadoop"
]


DOMAIN_KEYWORDS = [
    "payment-service",
    "order-service",
    "notification-service",
    "database",
    "db",
    "timeout",
    "latency",
    "retry",
    "connection pool",
    "memory leak",
    "pod restart",
    "5xx",
    "error",
    "cpu",
    "health"
]


def build_vectorstore():
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.*",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(
        split_docs,
        embeddings
    )

    vectorstore.save_local(VECTORSTORE_PATH)

    return vectorstore


def load_vectorstore():
    embeddings = OpenAIEmbeddings()

    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def is_context_relevant(query, docs):
    query_lower = query.lower()

    if any(term in query_lower for term in UNSUPPORTED_TERMS):
        return False

    combined_text = " ".join(
        [doc.page_content.lower() for doc in docs]
    )

    return any(
        keyword in combined_text
        for keyword in DOMAIN_KEYWORDS
    )


def retrieve_context(query, vectorstore, k=3):
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        log_retrieval(query, [])
        return None, []

    if not is_context_relevant(query, results):
        log_retrieval(query, [])
        return None, []

    context_parts = []
    sources = []

    for doc in results:
        source = doc.metadata.get("source", "unknown")
        sources.append(source)

        context_parts.append(
            f"Source: {source}\nContent:\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    log_retrieval(query, sources)

    return context, sources


def log_retrieval(query, sources):
    os.makedirs("logs", exist_ok=True)

    with open(RETRIEVAL_LOG_FILE, "a", encoding="utf-8") as file:
        file.write("\n==============================\n")
        file.write(f"Timestamp: {datetime.now()}\n")
        file.write(f"Query: {query}\n")
        file.write("Retrieved Sources:\n")

        if sources:
            for source in sources:
                file.write(f"- {source}\n")
        else:
            file.write("- No relevant sources found\n")