### **Frontend**
* **Framework:** React
* **Styling:** Tailwind CSS (Mobile-first responsive layout)
* **Integrations:** Google Calendar for Scheduling

### **Backend**
* **Framework:** FastAPI (Python 3.11+)
* **Vector Store / Retrieval:** bedrock / `pgvector` hybrid search
* **Embeddings & LLMs:** Amazon Titan / Lama 7b / Claude 3.5 Sonnet
* **Orchestration:** None

---

## 🚀 Quickstart Guide

### Prerequisites

* **Node.js** v18.x or higher
* **Python** 3.11+
* **Aws API Key** (or configured local model provider)

---

### 1. Backend Setup

```bash
uvicorn app.main:app --reload 
npm run dev
build.sh building