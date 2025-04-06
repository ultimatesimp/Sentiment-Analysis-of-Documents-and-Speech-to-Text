# 📄 Speech and Document Sentiment Analyzer

A project developed during the GCP Summer Course that leverages Google Cloud's AI/ML tools to analyze sentiment from either PDFs or audio files. This application extracts text from documents or audio, and classifies the sentiment using a custom-trained model hosted on Vertex AI.

## 🚀 Features

- 📄 **Document Sentiment Analysis**: Uses GCP Document AI to extract text from PDF files.
- 🔊 **Speech Sentiment Analysis**: Transcribes audio files into text using GCP Speech-to-Text API.
- 🤖 **Sentiment Classification**: Predicts whether the extracted text conveys a positive or negative sentiment using a Vertex AI model.

---

## 🧠 Model Overview

- **Model Type**: Custom text sentiment classifier.
- **Framework**: Google AutoML / Vertex AI.
- **Labels**: Binary (0 = Negative, 1 = Positive).
- **Training Data**: A custom dataset derived from various public review and sentiment datasets.

---

## 📁 Project Structure

```bash
├── documentai.py               # PDF processing & sentiment prediction
├── sc_gcp_project.py           # Audio processing pipeline
├── sentiment_prediction.py     # Vertex AI sentiment inference utility
├── transcripts/                # Stores transcribed text files
├── audio/                      # Local audio input files
└── README.md
```

---

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Google Cloud account with:
  - Document AI Processor
  - Vertex AI endpoint
  - Speech-to-Text API enabled
- Required libraries:
  ```bash
  pip install google-cloud-storage google-cloud-speech google-cloud-aiplatform pydub
  ```

- Add your service account key JSON and update the paths in:
  - `documentai.py`
  - `sc_gcp_project.py`

---

## 📘 Usage

### 1. Analyze PDF

```bash
python documentai.py
```

- Prompts for the file path to a PDF.
- Extracts text using Document AI.
- Sends the text to a deployed sentiment analysis model.
- Displays predicted sentiment.

### 2. Analyze Audio

```bash
python sc_gcp_project.py
```

- Reads `.wav` files from the `audio/` directory.
- Uploads to a GCP bucket and uses Speech-to-Text API for transcription.
- Transcribed text is saved and analyzed for sentiment.
- Outputs prediction to the console.

---

## 🔎 Example Output

```bash
Extracted Text:
"This product is amazing and easy to use."

Prediction:
{ 'sentiment': 1 }  # Positive
```

---

## 👨‍💻 Authors

- Akella Aditya Bhargav (PES2UG19CS024)
- Ankit P Bisleri (PES2UG19CS048)
- Anvesh S K (PES2UG19CS056)

---

## 📦 Acknowledgements

- Google Cloud Platform
- Vertex AI & AutoML
- Document AI
- Speech-to-Text API
