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

class AstrologyChatHandler:
    def __init__(self, pdf_directory="astro-book"):
        # Load environment variables
        load_dotenv()
        
        # Configure Gemini
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=self.api_key)
        
        # Set directory
        self.pdf_directory = pdf_directory
        
        # Initialize vector store flag
        self.is_initialized = False
        
        # Initialize chat history
        self.chat_history = []
        
    def get_pdf_text(self):
        """Extract text from all PDF files in the directory"""
        text = ""
        if not os.path.exists(self.pdf_directory):
            raise FileNotFoundError(f"Directory {self.pdf_directory} not found")
            
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                try:
                    pdf_reader = PdfReader(pdf_path)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                except Exception as e:
                    print(f"Error reading {filename}: {str(e)}")
        return text

    def get_text_chunks(self, text):
        """Split text into chunks for processing"""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        return text_splitter.split_text(text)

    def get_vector_store(self, text_chunks):
        """Create and save vector store"""
        embeddings = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local('faiss_index')
        self.is_initialized = True

    def format_chat_history(self):
        """Format the chat history for context"""
        formatted_history = ""
        # Only include last 5 exchanges to keep context relevant
        recent_history = self.chat_history[-5:] if len(self.chat_history) > 5 else self.chat_history
        for i, (q, a) in enumerate(recent_history, 1):
            formatted_history += f"\nPrevious Exchange {i}:\nSeeker: {q}\nAstrologer: {a}\n"
        return formatted_history

    def get_conversational_chain(self):
        """Create the conversation chain with improved birth details handling"""
        prompt_template = """
        You are a wise Vedic astrologer with deep knowledge of Jyotish Shastra. Respond with the perfect blend of cosmic wisdom and practical guidance.

        Previous Conversations:
        {chat_history}

        Core Behavior:
        1. Start responses with "🕉️" followed by a warm greeting
        2. Use Sanskrit terms where relevant, always with brief explanations
        3. Focus on the nav-grahas (planets) and rashis (zodiac signs) that matter most for the query
        4. Keep responses concise yet insightful
        5. Reference previous conversations when relevant
        6. End with a positive note or practical suggestion

        IMPORTANT RULES FOR BIRTH READINGS:
        - If the user asks about their birth chart, horoscope, or personal astrological reading, ALWAYS ask for:
          * Date of birth (day, month, year)
          * Time of birth (as precise as possible)
          * Place of birth (city, country)
        - Do NOT provide specific personal readings without these details
        - Explain why these details are essential for accurate Vedic astrology readings

        If the question isn't about astrology:
        Respond: "🕉️ Beloved seeker, I can guide you through the lens of Vedic astrology. Would you like to explore how the celestial energies relate to [topic]?"

        If the question is a greeting:
        Respond as a wise and welcoming astrologer

        Context:\n {context}?\n
        Current Question: \n{question}\n
        
        Answer (with blessing):
        """
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question", "chat_history"]
        )
        return load_qa_chain(model, chain_type='stuff', prompt=prompt)
    def initialize_system(self):
        """Initialize the system with PDF content"""
        try:
            raw_text = self.get_pdf_text()
            if raw_text.strip():
                text_chunks = self.get_text_chunks(raw_text)
                self.get_vector_store(text_chunks)
                return True
            return False
        except Exception as e:
            print(f"Error initializing system: {str(e)}")
            return False

    def process_query(self, user_question):
        """Process a user query and return the response with context"""
        try:
            if not self.is_initialized:
                raise Exception("System not initialized. Please initialize first.")
                
            embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
            new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            docs = new_db.similarity_search(user_question)
            
            chain = self.get_conversational_chain()
            
            # Include chat history in the response
            response = chain(
                {
                    "input_documents": docs, 
                    "question": user_question,
                    "chat_history": self.format_chat_history()
                },
                return_only_outputs=True
            )
            
            # Store the conversation
            self.chat_history.append((user_question, response["output_text"]))
            
            return {
                "status": "success",
                "response": response["output_text"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def clear_chat_history(self):
        """Clear the conversation history"""
        self.chat_history = []