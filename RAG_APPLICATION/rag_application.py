import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv  
load_dotenv()
from langchain_core.documents import Document


st.title("⚡ Quick RAG App (Chroma + Streamlit)")

# ChromaDB folder
PERSIST_DIR = "chroma_store"

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# ----------------------------
# Step 1: Upload + Index PDF
# ----------------------------
st.subheader("📤 Upload PDF to Store in ChromaDB")

uploaded = st.file_uploader("Upload your PDF", type="pdf")

if uploaded:
    pdf = PdfReader(uploaded)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""

    st.success("PDF Loaded Successfully!")

    if st.button("📌 Store PDF in Chroma"):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        chunks = splitter.split_text(text)


# convert to Document objects
        docs = [Document(page_content=c) for c in chunks]
        # docs = [{"page_content": c} for c in chunks]

        db = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )

        # db.persist()
        st.success(f"Stored {len(chunks)} chunks in ChromaDB!")


# ----------------------------
# Step 2: Ask Questions (Query)
# ----------------------------
st.subheader("❓ Ask Question from PDF")

query = st.text_input("Enter your question:")

if st.button("🔍 Get Answer"):
    db = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(query)

    if not docs:
        st.error("No answer found in the vector store!")
    else:
        context = "\n\n".join([d.page_content for d in docs])
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        prompt = f"""
        You are a RAG assistant.
        Use the following context to answer the question:

        CONTEXT:
        {context}

        QUESTION:
        {query}
        """

        answer = llm.invoke(prompt)

        st.write("### ✅ Answer:")
        st.write(answer.content)

        st.write("---")
        st.write("### 📚 Retrieved Chunks:")
        for d in docs:
            st.text(d.page_content[:300] + "...")
