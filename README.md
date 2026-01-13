# 🚀 JobPulse: Job Market Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Status](https://img.shields.io/badge/Status-Production-success)

**JobPulse** is an automated ETL pipeline and dashboard that tracks real-time job market trends (salaries, demand, remote work ratios). It features a self-healing data ingestion engine and a specialized dashboard for market analysis.

---

## 🏗 Architecture

The system follows a decoupled **Production Architecture**:

1.  **Ingestion Layer (`src/ingestion.py`):** - Runs nightly via **GitHub Actions**.
    - Fetches data from external APIs (Adzuna) or falls back to synthetic data.
    - Performs data cleaning and validation.
2.  **Storage Layer (`data/jobs.db`):** - SQLite database serving as the Single Source of Truth.
    - Updated automatically via CI/CD pipelines.
3.  **Presentation Layer (`app.py`):** - Streamlit dashboard optimized for read-heavy operations.
    - Zero-latency rendering using cached database connections.

---

## 🛠 Prerequisites

Before running the project locally, ensure you have:
* Python 3.9+
* Git
* (Optional) An Adzuna API Key (for real data)

## 💻 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/JobPulse.git](https://github.com/YOUR_USERNAME/JobPulse.git)
    cd JobPulse
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize Database (First Run)**
    ```bash
    python -m src.ingestion
    ```

5.  **Launch Dashboard**
    ```bash
    streamlit run app.py
    ```

---

## 🐳 Docker Support

To run the application in an isolated container:

```bash
# Build the image
docker build -t jobpulse .

# Run the container
docker run -p 8501:8501 jobpulse