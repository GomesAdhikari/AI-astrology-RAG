from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_pdf_text(pdf_directory):
    text = ""
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            try:
                pdf_reader = PdfReader(pdf_path)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            except Exception as e:
                print(f"Error reading {filename}: {str(e)}")
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local('faiss_index')

def get_conversational_chain():
    prompt_template = """
    Assume you are an AI astrologer Answer the question asked you by the person as if it is an astrology query
    and if the question is not related to astrology simply say i am not authorised to answer
    and be as polite as possible, the talking style should be of a vedic Astrologer, as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type='stuff', prompt=prompt)
    return chain

def process_query(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    return response["output_text"]

def initialize_system(pdf_directory):
    print("Initializing system with PDFs...")
    raw_text = get_pdf_text(pdf_directory)
    if raw_text.strip():
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        return True
    else:
        print(f"No PDF files found in {pdf_directory}")
        return False

def main():
    pdf_directory = "astro-book"
    
    # Initialize the system
    if not initialize_system(pdf_directory):
        print("System initialization failed. Please check your PDF directory.")
        return

    print("\nAstrology Chat System Initialized!")
    print("Type 'quit' to exit the chat")
    
    while True:
        user_question = input("\nAsk your question: ").strip()
        
        if user_question.lower() == 'quit':
            print("Thank you for using the Astrology Chat System. Goodbye!")
            break
            
        if user_question:
            try:
                response = process_query(user_question)
                print("\nAstrologer's Response:", response)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()