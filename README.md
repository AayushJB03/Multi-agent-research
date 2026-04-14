# 🔬 ResearchMind: Multi-Agent Research Pipeline

ResearchMind is an advanced AI-powered research assistant built using **LangChain**, **LangGraph**, and **Google Gemini 2.5 Flash**. It automates the complex process of researching topics by employing multiple specialized AI agents to search the web, extract content, synthesize comprehensive reports, and critically review the final output. 

Both a sleek **Streamlit** user interface and a command-line interface are provided.

---

## ✨ Features

- **Multi-Agent Architecture**: Uses `create_react_agent` to orchestrate agents for specific subtasks.
- **Automated Web Searching**: Leverages the **Tavily API** to hunt for the most recent, relevant sources based on your research topic.
- **Intelligent Scraping**: A dedicated reader agent crawls selected URLs and uses **BeautifulSoup** to extract clean content, skipping over navbars, footers, and scripts.
- **Synthesized Report Generation**: Compiles search results and scraped content into a well-structured final report (Introduction, Key Findings, Conclusion, Sources).
- **Critic Review**: A final independent evaluator pipeline reviews the generated report with a strict scoring matrix, identifying strengths and areas for improvement.
- **Modern Web Interface**: Enjoy a premium, dark-mode Streamlit UI that provides real-time progress indicators and detailed output cards.

---

## 🏗️ Architecture / Pipeline Steps

1. **Search (Agent 1)**: `web_search` tool queries Tavily for up to 5 highly relevant snippets and URLs.
2. **Read (Agent 2)**: `web_scrape` tool picks top URLs from the search results, extracts the HTML, and cleans the text strings.
3. **Write (Chain 1)**: LangChain's LCEL combines the context into a prompt to draft a fully formatted final report via Gemini.
4. **Critic (Chain 2)**: Evaluates the report drafted in Step 3 and outputs a critique score out of 10.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.9+**
- Active API keys for:
  - [Google Gemini API](https://aistudio.google.com/) (`GEMINI_API_KEY`)
  - [Tavily Search API](https://tavily.com/) (`TAVILY_API_KEY`)

---

## 🚀 Installation & Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/AayushJB03/Multi-agent-research.git
   cd Multi-agent-research
   ```

2. **Create a virtual environment (Recommended)**:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

---

## 💻 Running the Application

### 1. Streamlit Web App (Recommended UI)
To launch the interactive web interface, run:
```bash
streamlit run app.py
```
This will open `http://localhost:8501` in your default browser. Enter a topic in the search bar and watch the agents work through the pipeline step-by-step!

### 2. Command-Line Interface
If you prefer researching via terminal:
```bash
python pipeline.py
```
You will be prompted to enter a topic, and the raw findings, scraped content, and generated reports will execute sequentially right in the console output.

---

## 📂 Project Structure

```text
Multi-agent-research/
├── agents.py           # Core agent definitions and Prompt Templates (Search, Read, Write, Critic)
├── pipeline.py         # Orchestrates the agents into a 4-step execution flow
├── tools.py            # Langchain tool definitions (Tavily search & BS4 scraping)
├── app.py              # The Streamlit web user interface
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API keys)
└── .gitignore          # Ignored files/folders
```

---

## 📝 License

This project is licensed under the MIT License.