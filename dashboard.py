
import streamlit as st


def show_dashboard():

    st.header("📊 Customer Support Dashboard")

    total_messages = len(
        st.session_state.get("messages", [])
    )

    total_documents = len(
        st.session_state.get("company_documents", [])
    )

    total_chunks = len(
        st.session_state.get("document_chunks", [])
    )

    total_tickets = (
        1 if "support_ticket" in st.session_state else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Chat Messages", total_messages)
    col2.metric("Documents", total_documents)
    col3.metric("Text Chunks", total_chunks)
    col4.metric("Support Requests", total_tickets)

    st.divider()

    st.subheader("Knowledge Base Status")

    if st.session_state.get("vector_index") is not None:
        st.success("Knowledge base is ready.")
    else:
        st.warning("No knowledge base is currently loaded.")

    st.subheader("Conversation Status")

    if total_messages > 1:
        st.success("Conversation is active.")
    else:
        st.info("No customer conversation yet.")

    st.subheader("Human Support Status")

    if "support_ticket" in st.session_state:
        st.warning("A support request is awaiting human review.")
    else:
        st.info("No support requests in this session.")
