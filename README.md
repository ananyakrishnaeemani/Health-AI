# 🏥 AI Powered Health Assistant 
**You can try the deployed version of my chatbot here:** [https://ai-healthassistant.streamlit.app/](https://ai-healthassistant.streamlit.app/)

## Installation and Setup

Follow these steps to set up and run the chatbot locally:

### 1. Clone the Repository
```bash
git clone [your-repo-link]
cd [your-repo-folder]
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Generate API Keys
- **Pinecone API**: Sign up on [Pinecone](https://www.pinecone.io/) and generate an API key.
- **Groq API**: Obtain your API key from [Groq](https://groq.com/).

### 4. Connect to Pinecone and Create Vector Database
Modify the `.env` file with your Pinecone API key and Groq API key. Then, run the following command to create the vector database:
```bash
python store_index.py
```

### 5. Run this Flask UI
```bash
python app.py
```

### 6. Run the Streamlit UI
Launch the chatbot interface using Streamlit:
```bash
streamlit run app_stream.py
```

## 🚀 Features
- **Symptom Checker:** AI-powered symptom analysis and health insights.
- **AI-Powered Chatbot:** Get instant answers to health-related queries.
- **Health Query Resolution** Responds to user queries with AI-generated medical insights.
- **Symptom-Based Assistance**  Provides preliminary guidance on symptoms and possible
conditions.
- **Conversational Memory**  Retains chat history for an improved user experience.
- **Secure and Scalable Architecture**  Ensures data security and efficient handling of multiple
queries.

## 🛠️ Tech Stack
- **Frontend:** Streamlit 
- **Backend:** Large Language Model, Retrieval-Augmented Generation
- **AI Integration:** Groq API, Pinecone API
- **Deployment:** Streamlit

## 📞 Contact
**Ananya Krishna** via [LinkedIn](https://www.linkedin.com/in/ananyakrishna/) or email at **ananyakrish124@gmail.com**.

