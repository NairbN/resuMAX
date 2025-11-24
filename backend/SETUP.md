# ResuMAX Backend Setup Guide

## Prerequisites
1.  **Docker Desktop**: Download and install from [docker.com](https://www.docker.com/products/docker-desktop/).
2.  **Git**: To clone the repository.

## Quick Start (Recommended)
This method runs the backend in a container, so you don't need to install Python or manage virtual environments manually.

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd resuMAX/backend
    ```

2.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```

3.  **Verify**:
    Open your browser to [http://localhost:8080/health](http://localhost:8080/health). You should see `{"status": "ok"}`.

    The API is now ready to accept requests from your frontend!

---

## Alternative: Local Python Setup (Windows/Mac/Linux)
If you want to run the **Desktop GUI** or develop without Docker:

1.  **Install Python 3.11+**.
2.  **Create a virtual environment**:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Backend**:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
5.  **Run Desktop GUI** (Optional):
    ```bash
    python desktop_gui.py
    ```
