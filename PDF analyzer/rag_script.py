import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. CONFIGURATION (Ensure you use the correct embedding model)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCZHb7parrIiZUVk27eikeT5YYIe54F1xU"

def build_knowledge_base(path="./pdfs"):
    print("--- 📚 Processing Semester PDFs ---")
    loader = DirectoryLoader(path, glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    
    # Precise splitting for Viva questions
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    
    # IMPORTANT: Use 'gemini-embedding-001', NOT the chat model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("faiss_study_index")
    return vector_db

def format_docs(docs):
    """Formats retrieved chunks with citations for the AI to see."""
    context = ""
    for doc in docs:
        source = doc.metadata.get('source', 'Unknown File')
        page = doc.metadata.get('page', 0) + 1
        context += f"\n[Source: {source}, Page: {page}]\n{doc.page_content}\n"
    return context

def start_viva_session():
    # Load or build the DB
    if os.path.exists("faiss_study_index"):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        vector_db = FAISS.load_local("faiss_study_index", embeddings, allow_dangerous_deserialization=True)
    else:
        vector_db = build_knowledge_base()

    # The 2026 Model Choice
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    # The 2026 Prompt Design
    template = """You are a College Viva Examiner. Answer the student's question based ONLY on the context below. 
    If the answer isn't there, say "I couldn't find that in your semester notes."
    
    Context:
    {context}
    
    Student Question: {question}
    
    Detailed Answer (Include Citations):"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # THE 2026 LCEL PIPE (|) CHAIN
    rag_chain = (
        {"context": vector_db.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Run the viva
    query = input("\nAsk your viva question: ")
    print("\n--- ASSISTANT RESPONSE ---")
    print(rag_chain.invoke(query))

if __name__ == "__main__":
    start_viva_session()