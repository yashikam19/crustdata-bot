# crustdata-bot

This application demonstrates an intelligent question-answering system which enables developers to quickly get accurate answers about Crustdata's API endpoints, any technical questions related to the documentation, and common troubleshooting solutions.

### 🌐 [Streamlit Demo App](https://crustdata-api-buddy.streamlit.app/)

### 📄 [FastAPI Swagger Page (deployed on Render)](https://fastapi-deployment-suxs.onrender.com/docs)

## 🔍 Key features

* **Code Examples**: Includes properly formatted curl commands and JSON payloads for immediate use
* **Session Management**: Allows the user to create and manage different sessions with maintained chat history for each session


*  `Selenium` is used for scraping content from the website, including content from toggles, headers, hyperlinks, code blocks, and tables.
* `Chroma DB` is used as vector database to store, ingest and query documents.

## ⚡ Quickstart Guide

### 🛠️ Prerequisites

1. **Python**: Ensure Python is installed. You can download it from [here](https://www.python.org/downloads/).

### Setup Python environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yashikam19/crustdata-bot.git
   cd crustdata-bot
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv myenv
   myenv/Scripts/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the `.env` file with your API key:
   ```bash
   OPENAI_API_KEY="<Put your token here>"
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```
## 🧠 Example Queries for Streamlit App

**Question:**
Give some practice questions on chapter Sound

## 📘 Dataset Used

* https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48#3315bbdfa0054a2aa440e98bdec3ff90
* https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c#aa49c8b2a8ba4a05a49ca380fed4b95b
