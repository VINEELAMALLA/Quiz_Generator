# 🧠 AI Quiz Generator using LLM

## 🔹 Repository Description
An AI-powered quiz generator that uses Large Language Models (LLMs) to analyze input text and automatically generate structured quizzes for effective learning and assessment.

---

## 🚀 Overview

The AI Quiz Generator is an intelligent system that converts raw text into interactive quizzes using LLMs. It helps students, educators, and self-learners quickly create assessments from notes, articles, or study materials.

---

## ✨ Features

- 📄 Accepts any text input (notes, articles, PDFs, etc.)
- 🤖 Uses LLMs to understand and extract key concepts
- ❓ Generates different types of questions:
  - Multiple Choice Questions (MCQs)
  - True/False
  - Short Answer Questions
- ⚡ Fast and automated quiz generation
- 🎯 Improves learning through self-assessment

---

## 🧩 How It Works

1. User inputs text
2. The system processes and analyzes the content
3. LLM identifies important concepts and topics
4. Quiz questions are generated automatically
5. Output is displayed in a structured format

---

## 🛠️ Tech Stack

- Python
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- Streamlit (for UI - optional)
- OpenAI API / Hugging Face API

---

## 📂 Project Structure


AI-Quiz-Generator/
│
├── app.py # Main application file
├── quiz_generator.py # Core quiz generation logic
├── utils.py # Helper functions
├── requirements.txt # Dependencies
├── README.md # Documentation
└── data/ # Sample input files


---

## ⚙️ Installation

1. Clone the repository:

git clone https://github.com/your-username/ai-quiz-generator.git

cd ai-quiz-generator


2. Install dependencies:

pip install -r requirements.txt


3. Set up API key (if required):

export OPENAI_API_KEY=your_api_key


---

## ▶️ Usage

Run the application:


python app.py


Or with Streamlit UI:


streamlit run app.py


Steps:
- Input or upload text
- Click on "Generate Quiz"
- View the generated questions instantly

---

## 📸 Example

**Input:**

Machine learning is a subset of artificial intelligence that enables systems to learn from data.


**Output:**
What is machine learning?
Machine learning is a subset of which field?
a) Data Science
b) Artificial Intelligence
c) Robotics
d) Cybersecurity

---

## 🎯 Use Cases

- 📚 Students for exam preparation
- 👩‍🏫 Teachers for creating quizzes
- 🌐 EdTech platforms
- 🧠 Self-learning and revision

---

## 🔮 Future Improvements

- Difficulty level control (Easy / Medium / Hard)
- Topic-based quiz generation
- Multilingual support
- Voice-based quiz interaction
- Integration with LMS platforms
