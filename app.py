import streamlit as st
from dotenv import load_dotenv

from src.task10_generation import generate_with_citation


load_dotenv()

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("RAG Chatbot")
    st.caption("Thay mô tả theo đề tài của nhóm")
    top_k = st.slider("Số chunks", 3, 10, 5)

st.title("RAG Chatbot")
st.caption("Thay tiêu đề và hướng dẫn sử dụng")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption(f"Nguồn truy hồi: {message.get('retrieval_source', 'unknown')}")
            with st.expander("Xem nguồn"):
                for source in message["sources"]:
                    metadata = source.get("metadata", {})
                    st.markdown(
                        f"**{metadata.get('title', metadata.get('source', 'Unknown'))}** "
                        f"({metadata.get('source', 'Unknown')})"
                    )
                    st.caption(
                        f"Phương thức: {source.get('retrieval_method', 'unknown')} | "
                        f"Score: {source.get('score', 0):.4f}"
                    )

query = st.chat_input("Nhập câu hỏi...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        try:
            generation = generate_with_citation(query, top_k=top_k)
        except Exception:
            generation = {
                "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
                "sources": [],
                "retrieval_source": "none",
            }
        answer = generation["answer"]
        sources = generation.get("sources", [])
        st.markdown(answer)
        if sources:
            st.caption(f"Nguồn truy hồi: {generation.get('retrieval_source', 'unknown')}")
            with st.expander("Xem nguồn"):
                for source in sources:
                    metadata = source.get("metadata", {})
                    st.markdown(
                        f"**{metadata.get('title', metadata.get('source', 'Unknown'))}** "
                        f"({metadata.get('source', 'Unknown')})"
                    )
                    st.caption(
                        f"Phương thức: {source.get('retrieval_method', 'unknown')} | "
                        f"Score: {source.get('score', 0):.4f}"
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "retrieval_source": generation.get("retrieval_source", "none"),
        }
    )
