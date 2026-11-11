import streamlit as st
from document_processor import extract_pdf_text
from chatbot import generate_response
from chunking import create_chunks
from vector_store import build_vector_index
from vector_store import search_documents
from knowledge_base import (
    save_knowledge_base,
    load_knowledge_base
)

st.set_page_config(
    page_title="AI Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Customer Support Chatbot")
st.write("Welcome! Ask us anything about our products or services.")

# Initialize session state variables safely
if "company_documents" not in st.session_state:
    st.session_state["company_documents"] = []

if "document_chunks" not in st.session_state:
    st.session_state["document_chunks"] = []

if "vector_index" not in st.session_state:
    st.session_state["vector_index"] = None

# Load saved knowledge base once per session

if "knowledge_base_loaded" not in st.session_state:

    try:
        index, chunks = load_knowledge_base()

        if index is not None:
            st.session_state["vector_index"] = index
            st.session_state["document_chunks"] = chunks

            st.sidebar.success(
                f"Loaded {len(chunks)} saved document chunks."
            )

        st.session_state["knowledge_base_loaded"] = True

    except Exception as error:
        st.sidebar.error(
            f"Knowledge base loading failed: {error}"
        )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Welcome to Customer Support. How can I help you today?"
        }
    ]

# COMPANY DOCUMENT UPLOAD (Sidebar)
st.sidebar.header("📚 Company Knowledge Base")

uploaded_documents = st.sidebar.file_uploader(
    "Upload company PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

if st.sidebar.button("Process Documents"):
    if not uploaded_documents:
        st.sidebar.warning("Please upload at least one PDF.")
    else:
        with st.sidebar.spinner("Extracting document text and chunking..."):
            try:
                company_documents = []
                for document in uploaded_documents:
                    pages = extract_pdf_text(document)
                    company_documents.append({
                        "filename": document.name,
                        "pages": pages
                    })

                # Save raw docs and generated chunks to session state
                st.session_state["company_documents"] = company_documents
                
                chunks = create_chunks(
                    company_documents,
                    chunk_size=500,
                    overlap=75
                )
                
                if not chunks:
                    st.sidebar.warning("No text chunks were created.")
                else:
                    vector_index = build_vector_index(chunks)

                    # Save knowledge base permanently
                    save_knowledge_base(vector_index, chunks)

                    # Update Streamlit session state
                    st.session_state["document_chunks"] = chunks
                    st.session_state["vector_index"] = vector_index

                    st.sidebar.success("Knowledge base saved successfully!")
                    st.sidebar.success(f"Processed {len(company_documents)} document(s).")
                    st.sidebar.success(f"Created and indexed {len(chunks)} text chunks.")
            except Exception as error:
                st.sidebar.error(f"Document processing failed: {error}")

# DISPLAY PROCESSED DOCUMENTS EXPANDER
if st.session_state["company_documents"]:
    st.subheader("📚 Processed Company Documents")
    for document in st.session_state["company_documents"]:
        with st.expander(document["filename"]):
            for page in document["pages"]:
                st.write(f"**Page {page['page']}**")
                st.write(page["text"])

# DISPLAY DOCUMENT CHUNKS
if st.session_state["document_chunks"]:
    st.subheader("🧩 Document Text Chunks")
    st.write(f"Total chunks created: {len(st.session_state['document_chunks'])}")
    
    for index, chunk in enumerate(st.session_state["document_chunks"]):
        with st.expander(f"Chunk {index + 1}"):
            st.write(f"File: {chunk['filename']}")
            st.write(f"Page: {chunk['page']}")
            st.write(chunk["text"])

st.divider()

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input & response handling

# User input & response handling

if user_question := st.chat_input("Type your question here..."):

    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching company documents and generating answer..."):

            try:
                # STEP 1: Retrieve relevant company information
                search_results = []

                if (
                    st.session_state.get("vector_index") is not None
                    and st.session_state.get("document_chunks")
                ):

                    search_results = search_documents(
                        query=user_question,
                        index=st.session_state["vector_index"],
                        chunks=st.session_state["document_chunks"],
                        top_k=3
                    )

                # STEP 2: Display retrieved information
                if search_results:

                    with st.expander("🔍 Retrieved Company Information"):

                        for result in search_results:

                            st.write(f"**File:** {result['filename']}")
                            st.write(f"**Page:** {result['page']}")
                            st.write(f"**Similarity:** {result['score']:.4f}")
                            st.write(result["text"])
                            st.divider()

                # STEP 3: Generate AI answer using retrieved information
                assistant_response = generate_response(
                    messages=st.session_state.messages,
                    search_results=search_results
                )

                # STEP 4: Display AI response
                st.write(assistant_response)

                # STEP 5: Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

            except Exception as error:

                st.error(f"AI response failed: {error}")
