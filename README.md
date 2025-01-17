# crustdata-bot

This application demonstrates an intelligent question-answering system which enables developers to quickly get accurate answers about Crustdata's API endpoints, any technical questions related to the documentation, and common troubleshooting solutions.

The repository is composed of three main segments:
1. [web-scraper](https://github.com/yashikam19/crustdata-bot/tree/main/web-scraper): Selenium-based scraping of Crustdata's API documentation Notion webpage.
2. [rag-backend](https://github.com/yashikam19/crustdata-bot/tree/main/rag-backend): FastAPI backend hosted on Render.
3. [streamlit-frontend](https://github.com/yashikam19/crustdata-bot/tree/main/streamlit-frontend): A simple chat interface with session management deployed using Streamlit.

### 🌐 [Streamlit Demo App](https://crustdata-api-buddy.streamlit.app/)

### 📄 [FastAPI Swagger Page](https://fastapi-deployment-suxs.onrender.com/docs)

## 🔍 Key features

* **Code Examples**: Includes properly formatted curl commands and JSON payloads for immediate use
* **Session Management**: Allows the user to create and manage different sessions with maintained chat history for each session


*  `Selenium` is used for scraping content from the website, including content from toggles, headers, hyperlinks, code blocks, and tables.
* `Chroma DB` is used as vector database to store, ingest, and retrieve documents using vector based similarity search.
* The application uses OpenAI's `gpt-4o-mini` model for generation.

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

**Question 1:**

<img width="858" alt="error_1" src="https://github.com/user-attachments/assets/2e5c8511-ca96-45d2-bf42-9ca3e15c92e6" />
<img width="827" alt="error2" src="https://github.com/user-attachments/assets/a89df59e-1b47-4fcc-9748-fa4939409983" />
<img width="740" alt="error3" src="https://github.com/user-attachments/assets/c1e22c39-a83b-4837-98ed-6dc1d69ec082" />


* The response immediately points out the exact issue: the invalid type parameter
* Follows with comprehensive reference information: lists ALL valid operators, not just the one needed


**Question 2:** How to search for LinkedIn posts that contain specific keywords?

<img width="856" alt="table_part1" src="https://github.com/user-attachments/assets/776a2651-a34a-4258-a9d9-f3b6bce588ee" />
<img width="853" alt="table_part2" src="https://github.com/user-attachments/assets/266e47eb-5ade-4b3a-9306-4168f02038fe" />


* The response clearly states the required endpoint.
* It provides a detailed description of the query by including the response body, curl command and key points


**Question 3:**

<img width="374" alt="1" src="https://github.com/user-attachments/assets/6860f25e-de45-4460-b77f-27d87396aeaa" />


* The response includes a link to the reference list


## 📘 Dataset Used

* https://crustdata.notion.site/Crustdata-Discovery-And-Enrichment-API-c66d5236e8ea40df8af114f6d447ab48#3315bbdfa0054a2aa440e98bdec3ff90
* https://crustdata.notion.site/Crustdata-Dataset-API-Detailed-Examples-b83bd0f1ec09452bb0c2cac811bba88c#aa49c8b2a8ba4a05a49ca380fed4b95b
