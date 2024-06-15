import PyPDF2
import nltk
import re
import string
import json
import pickle
import warnings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai

# Download NLTK resources
warnings.filterwarnings("ignore", category=FutureWarning)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Initialize Sentence Transformer model
MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# OpenAI API key (replace with your actual key)
openai.api_key = "your_key"

# Function to fix word spacing issues in extracted text
def fix_word_spacing(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase followed by uppercase
    text = re.sub(r'([a-z])(\d)', r'\1 \2', text)  # Add space between lowercase followed by digit
    text = re.sub(r'(\d)([a-z])', r'\1 \2', text)  # Add space between digit followed by lowercase
    text = re.sub(r'(\d)([A-Z])', r'\1 \2', text)  # Add space between digit followed by uppercase
    text = re.sub(r'([a-z])([,.:;!?])', r'\1 \2', text)  # Add space between lowercase followed by punctuation
    text = re.sub(r'([A-Z])([a-z])', r'\1 \2', text)  # Add space between uppercase followed by lowercase
    return text

# Function to clean and preprocess text
def clean_text(text):
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')

    text = text.lower()  # Convert to lowercase
    text = re.sub(r'^RT[\s]+', '', text)  # Remove old style retweet text "RT"
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)  # Remove hyperlinks
    text = re.sub(r'#', '', text)  # Remove hashtags

    tokens = word_tokenize(text)  # Tokenize text

    texts_clean = []
    for word in tokens:
        if word not in stopwords_english and word not in string.punctuation:
            stem_word = stemmer.stem(word)  # Stemming
            texts_clean.append(stem_word)

    text_clean = ' '.join(texts_clean)  # Join cleaned tokens
    return text_clean

# Function to extract text from a PDF and save it to a file
def extract_text_from_pdf_save_it(pdf_path, output_txt_path):
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as file_txt:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        text = clean_text(fix_word_spacing(text))
                        file_txt.write(text + ' ')
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
    except Exception as e:
        print(e)

# Function to encode sentences using Sentence Transformer and save to file
def save_encodings(sentences, filename):
    try:
        encodings = MODEL.encode(sentences)
        with open(filename, 'wb') as file:
            pickle.dump(encodings, file)
    except Exception as e:
        print(f"Error saving encodings to {filename}: {e}")

# Function to load encodings from file
def load_encodings(filename):
    try:
        with open(filename, 'rb') as file:
            encodings = pickle.load(file)
        return encodings
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error loading encodings from {filename}: {e}")
        return None

# Function to generate batches of text data
def text_batch_generator(text, batch_size=4000):
    start_idx = 0
    end_idx = batch_size

    while start_idx < len(text):
        batch = text[start_idx:end_idx]
        yield batch
        start_idx = end_idx
        end_idx += batch_size

# Function to save batches of text to a JSON file
def save_batches(input_text, output_json_path):
    try:
        batches = list(text_batch_generator(input_text))
        with open(output_json_path, 'w') as file:
            json.dump(batches, file)
    except Exception as e:
        print(f"Error saving batches to {output_json_path}: {e}")

# Function to select relevant batches based on similarity to target sentence
def select_batches(t_sentence: str, check_sent):
    model = MODEL
    target_sent = model.encode([t_sentence])
    
    # Reshape to 2D arrays if needed
    if len(target_sent.shape) == 1:
        target_sent = target_sent.reshape(1, -1)
    if len(check_sent.shape) == 1:
        check_sent = check_sent.reshape(1, -1)
    
    similarity_scores = cosine_similarity(target_sent, check_sent)[0]
    
    if np.max(similarity_scores) >= 0.4:
        top_indices = [np.argmax(similarity_scores)]
    else:
        top_indices = np.argsort(similarity_scores)[-2:][::-1]
    
    return top_indices.tolist()

# Function to interact with GPT-3.5 API and provide responses
def gpt_tutor(messages):
    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5
        )
        ai_response = chat.choices[0].message['content']
        messages.append({"role": "assistant", "content": ai_response})
        return ai_response, messages
    except Exception as e:
        print(f"Error interacting with GPT-3.5 API: {e}")
        return "", messages

# Function to get the full text of the book
def get_book_text():
    with open(output_txt_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to get a specific batch of text based on index
def get_batch(index=None):
    with open(output_json_path, 'r', encoding='utf-8') as file:
        batches = json.load(file)
        if index is not None:
            return batches[index]
        return batches

# Main program
if __name__ == "__main__":
    pdf_path = r"H:\RAW Projects\Tutor-AI-for-Doubts\resources\ncert_history.pdf"
    output_txt_path = r"H:\RAW Projects\Tutor-AI-for-Doubts\resources\book.txt"
    output_json_path = r"H:\RAW Projects\Tutor-AI-for-Doubts\resources\batches.json"
    encodings_filename = r"H:\RAW Projects\Tutor-AI-for-Doubts\resources\encodings_batches.pkl"

    try:
        extract_text_from_pdf_save_it(pdf_path, output_txt_path)
        with open(output_txt_path, 'r', encoding='utf-8') as file:
            book_text = file.read()

        save_batches(book_text, output_json_path)
        save_encodings(book_text, encodings_filename)
        encodings = load_encodings(encodings_filename)

        base_context = """
        You are an educational tutor with a focus on providing insightful explanations and answering questions related to various concepts.
        Your primary goal is to assist users in understanding topics effectively and resolving their doubts.
        Provide clear, detailed, and insightful explanations.
        You will be given specific context or topics to address.
        Use simple, easy-to-understand language.
        Provide examples, analogies, and step-by-step explanations when necessary.
        """
        messages = [{"role": "system", "content": base_context}]
        interaction = 0
        input_req = [
            {"student_input": "Who was Napoleon?", "teacher_response": ""},
            {"student_input": "Give me detailed answer for which wars did Napoleon win?", "teacher_response": ""},
            {"student_input": "Write about Indian History.", "teacher_response": ""}
        ]

        for dict_input in input_req:
            user_input = dict_input["student_input"]
            
            if interaction < 3:
                # Use small context for the first 3 interactions
                context_i = select_batches(user_input, encodings)
                if len(context_i) == 1:
                    context = get_batch(context_i[0])
                else:
                    context = get_batch(context_i[0]) + " " + get_batch(context_i[1])
                
                context_message = f"""
                The following excerpt from the book is most relevant to the question at hand.
                Use this specific context to address the doubt and provide a thorough, accurate response:
                {context}
                """
            else:
                # Use the full book context after 3 interactions
                context = get_book_text()
                context_message = f"""
                If the context provided from the part of the book is insufficient,
                utilize the complete book context related to the doubt to formulate a comprehensive response:
                {context}
                """
            
            messages.append({"role": "system", "content": context_message})
            messages.append({"role": "user", "content": user_input})
            response, messages = gpt_tutor(messages)
            dict_input["teacher_response"] = response
            interaction += 1

        print(json.dumps(input_req, indent=2))
    except Exception as e:
        print(f"Error in main program execution: {e}")
