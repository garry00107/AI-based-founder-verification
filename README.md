# 🚀 Startup Analyzer Suite

A Flask-based web application that analyzes startup and founder credibility using AI and external data sources.

---

## 🧱 Technology Stack

### 🔧 Core Technologies

- **Programming Language:** Python  
  - Backend logic, API interactions, AI processing, and app flow.
  - Chosen for its readability, rich ecosystem, and strong AI/data science libraries.

- **Web Framework:** Flask  
  - Handles routing, request/response flow, context management.
  - Modularized using Flask Blueprints.

---

### 🎨 Frontend Technologies

- **Templating Engine:** Jinja2  
  - Dynamic HTML rendering with Python expressions.
  - Includes a custom filter for number formatting.

- **Markup Language:** HTML5  
  - Forms, structure, and content of the user interface.

- **Styling Language:** CSS3  
  - Layout and appearance via `static/css/style.css`.

- **CSS Framework:** Bootstrap 5.3  
  - Responsive design and pre-built UI components.
  - Included via CDN in `base.html`.

---

### 🌐 Data Fetching & Web Interaction

- **HTTP Requests:** `requests`  
  - Interacts with external APIs (Crunchbase, OpenAI, etc.)

- **Web Scraping:** `BeautifulSoup4`  
  - Parses HTML content for data extraction (limited and unreliable use).

---

### 📡 External API Integrations

- **Crunchbase API**  
  - Structured startup and founder data (via API key).

- **OpenAI API**  
  - Generative AI tasks: SWOT, summaries (via `openai` Python library).

- **(Placeholders)**  
  - Bloomberg, Failory: Future scraping/integration.
  - Legal/Financial/KYC APIs: Reserved for scalable verification features.

---

### 🧠 AI / NLP Libraries

- **Hugging Face `transformers`**  
  - Pre-trained pipelines for:
    - Sentiment Analysis
    - Text Summarization

- **PyTorch (`torch`)**  
  - Backend for transformers, no direct usage.

- **spaCy**  
  - Fast NLP (Named Entity Recognition for PERSON, ORG, GPE, etc.)

- **scikit-learn** (Mentioned)  
  - For future machine learning features (e.g., fraud detection, success prediction).

---

### ⚙️ Configuration & Utilities

- **Environment Management:** `python-dotenv`  
  - Loads `.env` variables like API keys in `config/settings.py`.

- **Utilities:**  
  - `logging`, `json`, `datetime`, `re`: For logs, text processing, formatting.

---



