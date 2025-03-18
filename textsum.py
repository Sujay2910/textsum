import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
import PyPDF2
from docx import Document
import base64

# Ensure nltk punkt is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Set Page Configuration
st.set_page_config(
    page_title="Text Summarizer",
    page_icon="logo.png"
)


# Function to summarize text
def summarize_text(input_text, num_sentences=3):
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return "\n".join(str(sentence) for sentence in summary)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("data:image/png;base64,{base64_image}") no-repeat center center fixed;
                background-size: cover;
            }}
            .overlay {{
                background: rgba(0, 0, 0, 0.6);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            }}
            .stTextArea textarea {{
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #4CAF50;
            }}
            .stButton>button {{
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
                border: none;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
                transition: 0.3s;
            }}
            .stButton>button:hover {{
                background-color: #45a049;
                transform: scale(1.05);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set Background Image
set_background("back1.jpg")  # Ensure this image exists in your directory

st.markdown('<div class="overlay">', unsafe_allow_html=True)  # Start Overlay

st.title("📄 Text Summarizer")
st.write("Summarize text, PDFs, and Word documents quickly and efficiently!")

# Layout with two columns
col1, col2 = st.columns(2)

# Left Column: Manual Text Input
with col1:
    input_text = st.text_area("✍️ Enter text to summarize:", height=200)
    num_sentences = st.slider("🔢 Number of sentences in summary:", 1, 10, 3)
    if st.button("🚀 Summarize Text"):
        if input_text.strip():
            summary = summarize_text(input_text, num_sentences)
            st.text_area("📌 Summarized Text:", summary, height=250)
            
            # Download button for summary
            summary_bytes = summary.encode('utf-8')
            st.download_button(
                label="⬇️ Download Summary",
                data=summary_bytes,
                file_name="summarized_text.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please enter some text to summarize.")

# Right Column: File Upload Summarization
with col2:
    uploaded_file = st.file_uploader("📂 Upload a text, PDF, or Word file:", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        text_data = ""
        
        if file_extension == "txt":
            text_data = uploaded_file.read().decode("utf-8")
        elif file_extension == "pdf":
            text_data = extract_text_from_pdf(uploaded_file)
        elif file_extension == "docx":
            text_data = extract_text_from_docx(uploaded_file)
        
        if text_data:
            st.text_area("📃 Extracted Content:", text_data, height=150)
            if st.button("📌 Summarize File Text"):
                summary = summarize_text(text_data, num_sentences)
                st.text_area("📌 Summarized Text:", summary, height=250)
                
                # Download button for summarized file
                summary_bytes = summary.encode('utf-8')
                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary_bytes,
                    file_name="summarized_file_text.txt",
                    mime="text/plain"
                )
        else:
            st.error("❌ Could not extract text from the file.")

st.markdown('</div>', unsafe_allow_html=True)  # End Overlay
