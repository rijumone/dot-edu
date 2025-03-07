import os
import glob
import nltk
import numpy as np
from typing import List
from loguru import logger
import streamlit as st
from tqdm import tqdm
from rank_bm25 import BM25Okapi
from langchain_ollama import ChatOllama
# from langchain_deepseek import ChatDeepSeek
# from langchain_openai import ChatOpenAI

def get_ollama_llm(
        model_name: str = None,
        temperature: float = 0.8,
    ):
    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url=os.getenv('OLLAMA_URL'),
    )
    # llm = ChatOpenAI(
    #     model="deepseek/deepseek-r1:free",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     api_key=os.getenv('OPENROUTER_DEEPSEEK_API_KEY'),
    #     base_url='https://openrouter.ai/api/v1',
    # )
    return llm


def ask_llm(llm, query):
    response = llm.stream(f'{query}')
    return response


def read_markdown_chunks(files):
    """Reads markdown files and returns a list of chunks."""
    chunks = []
    for file in tqdm(files, desc="Reading Markdown Files"):
        with open(file, "r", encoding="utf-8") as f:
            chunks.append(f.read())  # Assumes each file is a chunk
    return chunks


def hybrid_search(query: str, top_k=2, alpha=0.5) -> List[str]:
    """Performs hybrid search using BM25 and embeddings, then combines results."""
    from qdrant_client import QdrantClient
    from langchain.embeddings import HuggingFaceEmbeddings
    
    nltk.download("punkt_tab")
    
    # Define embedding model
    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Initialize Qdrant client
    qdrant = QdrantClient(os.getenv('QDRANT_HOST'), api_key=os.getenv('QDRANT_API_KEY'))

    # BM25 search (retrieve top-k results)
    query_tokens = nltk.word_tokenize(query.lower())
    bm25_scores = st.session_state.bm25.get_scores(query_tokens)

    # Get top-k indices from BM25
    bm25_top_k_idx = np.argsort(bm25_scores)[::-1][:top_k]
    bm25_top_k_scores = [bm25_scores[i] for i in bm25_top_k_idx]
    
    # Embedding search in Qdrant
    query_embedding = st.session_state.embedding_model.embed_query(query)
    qdrant_results = qdrant.search(
        collection_name='apl-fin-500',
        query_vector=query_embedding,
        limit=top_k
    )

    # Extract Qdrant indices and scores
    qdrant_top_k_texts = [res.payload["text"] for res in qdrant_results]
    qdrant_top_k_scores = np.array([res.score for res in qdrant_results])

    # Normalize BM25 and Qdrant scores
    bm25_top_k_scores = np.array(bm25_top_k_scores) / max(bm25_top_k_scores) if max(bm25_top_k_scores) > 0 else np.zeros_like(bm25_top_k_scores)
    qdrant_top_k_scores = qdrant_top_k_scores / max(qdrant_top_k_scores)

    # Merge results (Hybrid score)
    hybrid_scores = alpha * bm25_top_k_scores + (1 - alpha) * qdrant_top_k_scores

    # Sort by final score
    sorted_indices = np.argsort(hybrid_scores)[::-1]

    # Return final ranked documents
    return [qdrant_top_k_texts[i] for i in sorted_indices]


def rerank_results(query: str, retrieved_docs: List[str]) -> List[str]:
    """Re-ranks retrieved documents based on query relevance."""
    from sentence_transformers import CrossEncoder

    # Load a re-ranking model
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    pairs = [(query, doc) for doc in retrieved_docs]
    scores = reranker.predict(pairs)
    
    # Sort docs by re-ranking score
    ranked_docs = [doc for _, doc in sorted(zip(scores, retrieved_docs), reverse=True)]
    
    return ranked_docs


def fetch_ranked_relevant_docs(query) -> List[str]:
    return rerank_results(query, hybrid_search(query))

def bm25_confidence(query, doc):
    """Returns BM25 score as confidence for a document."""
    query_tokens = query.split()
    return st.session_state.bm25.get_scores(query_tokens)[st.session_state.chunks.index(doc)]

def dense_confidence(query, doc):
    """Computes cosine similarity between query & document embeddings."""
    from sklearn.metrics.pairwise import cosine_similarity
    query_vector = np.array(st.session_state.embedding_model.embed_query(query)).reshape(1, -1)
    doc_vector = np.array(st.session_state.embedding_model.embed_query(doc)).reshape(1, -1)  # Use embed_query for single doc

    return cosine_similarity(query_vector, doc_vector)[0][0]  # Single similarity value


def hybrid_confidence(query, doc, alpha=0.5):
    """Combines BM25 and cosine similarity scores."""
    bm25_score = bm25_confidence(query, doc)
    dense_score = dense_confidence(query, doc)

    # Normalize BM25 to 0-1 range (min-max scaling)
    all_bm25_scores = [
        st.session_state.bm25.get_scores(
            query.split())[i] for i in range(len(st.session_state.chunks))]

    # Get min and max BM25 scores
    min_bm25 = min(all_bm25_scores)
    max_bm25 = max(all_bm25_scores)
    bm25_norm = (bm25_score - min_bm25) / (max_bm25 - min_bm25) if max_bm25 > min_bm25 else 0

    return alpha * bm25_norm + (1 - alpha) * dense_score

# Input Guardrail
def is_valid_input(user_query):
    """Check if input is non-toxic and relevant."""
    # from transformers import pipeline
    # toxicity_filter = pipeline("text-classification", model="unitary/unbiased-toxic-roberta")
    # toxicity_score = toxicity_filter(user_query)[0]["score"]
    # logger.info(f"Toxicity score: {toxicity_score}")
    # if toxicity_score > 0.5:
    #     return False, "Your input violates community guidelines."
    from better_profanity import profanity
    if profanity.contains_profanity(user_query):
        return False, "Your input violates community guidelines."
    return True, None

def main():
    # Read chunks and create BM25 index
    data_dir = "./financial-docs-md/chunks-500"
    md_files = glob.glob(f"{data_dir}/*.md")
    # print(md_files)
    if 'chunks' not in st.session_state:
        st.session_state.chunks = read_markdown_chunks(md_files)
    if 'bm25' not in st.session_state:
        st.session_state.bm25 = BM25Okapi([nltk.word_tokenize(chunk.lower()) for chunk in st.session_state.chunks])
    
    st.set_page_config(page_title='AAPL Financials Chatbot', page_icon='📈')
    st.title(" Think different")
    def chat_callback():
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        user_input = st.session_state.user_input
        valid, message = is_valid_input(user_input)
        if not valid:
            response_msg = {
                "role": "assistant",
                "content": message,
            }
            st.session_state.messages.append(response_msg)
            return
        
        logger.info(f'user_input: {user_input}')
        message = {
            "role": "user",
            "content": user_input,
        }
        st.session_state.messages.append(message)
        retrieved_docs = fetch_ranked_relevant_docs(user_input)
        st.sidebar.markdown(f'User query: ```{user_input}```')
        st.sidebar.markdown(f'Retrieved doc chunks:')
        for r_d in retrieved_docs:
            st.sidebar.markdown(f'- {r_d}')
            st.sidebar.markdown(f'Confidence: ```{round(hybrid_confidence(user_input, r_d),2)}```')
        st.sidebar.markdown('---')
        response_msg = {
            "role": "assistant",
            "content": ask_llm(
                st.session_state.llm,
                f'{retrieved_docs}\nQuestion: {user_input}',
            ),
        }
        st.session_state.messages.append(response_msg)

    # Add model selection dropdown
    available_models = [
        # "deepseek-r1:1.5b",
        # "deepseek-r1:7b",
        # "llama3.2:latest",
        # "llama3.2:1b",
        "phi4:latest",
        "gemma2:latest",
    ]
    selected_model = st.selectbox("Select AI Model", available_models, index=0)
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = selected_model

    
    if 'llm' not in st.session_state:
        st.session_state.llm = get_ollama_llm(
            st.session_state.selected_model,
        )



    st.chat_input(
        "Search AAPL financials",
        on_submit=chat_callback,
        key='user_input',
    )
    if 'messages' not in st.session_state:
        return

    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            # Handle rendering of generator, even tho Streamlit handles it automatically
            # but the string needs to be saved back to the message for continuity
            msg = message["content"]
            # check if msg is a generator
            if isinstance(msg, str):
                st.write(msg)
            else:
                ai_res_plchldr = st.empty()
                ai_response = ""
                for chunk in msg:
                    ai_response += chunk.content  # Append each chunk to the response text
                    ai_res_plchldr.write(ai_response)
                st.session_state.messages[idx]["content"] = ai_response



if __name__ == "__main__":
    main()
