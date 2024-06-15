# Tutor-AI-for-Doubts

## Overview

Tutor-AI-for-Doubts is an AI-based educational tutor designed to assist users in understanding various topics effectively and resolving their doubts. The system extracts text from a PDF book, processes it, and uses a combination of Sentence Transformers and OpenAI's GPT-3.5 to provide insightful explanations based on the content of the book.

## Features

- Extracts and preprocesses text from PDF files.
- Utilizes Sentence Transformers for semantic encoding of text.
- Generates contextually relevant responses using OpenAI's GPT-3.5 model.
- Provides small context excerpts for initial interactions and uses the complete book text if necessary.

## Requirements

- Python 3.6+
- PyPDF2
- NLTK
- Sentence Transformers
- Scikit-learn
- NumPy
- OpenAI Python client

## Installation

* Clone the repository:

    ```sh
    git clone https://github.com/yourusername/Tutor-AI-for-Doubts.git
    ```

## Usage

1. Replace the `pdf_path`, `output_txt_path`, `output_json_path`, and `encodings_filename` variables with the appropriate paths for your environment.

2. Replace the `openai.api_key` with your actual OpenAI API key.

3. Run the main script:

    ```sh
    python main.py
    ```

4. The program will extract text from the specified PDF, preprocess it, and generate responses for predefined questions.

## Project Structure

- `main.py`: Main script for extracting text, processing it, and interacting with GPT-3.5.
- `requirements.txt`: List of required Python packages.

## Example

An example input and output:

**Input:**
```json
{
  "student_input": "Who was Napoleon?",
  "teacher_response": ""
}
```

**Output:**
```json
{
  "student_input": "Who was Napoleon?",
  "teacher_response": "Napoleon Bonaparte was a French military and political leader who rose to prominence during the French Revolution..."
}
```

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT-3.5 model.
- [NLTK](https://www.nltk.org/) for natural language processing tools.
- [Sentence Transformers](https://www.sbert.net/) for the encoding model.
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) for PDF text extraction.
