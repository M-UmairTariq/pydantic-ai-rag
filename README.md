# Pydantic AI RAG

## About
This repository contains a Retrieval-Augmented Generation (RAG) system built with Python, leveraging PydanticAI agent for retrieval of revelant chunks and PostgreSQL with pgvector for efficient vector storage. The project aims to efficiently store, retrieve, and query data using AI models. It also includes Docker support for easy setup and management of PostgreSQL, pgvector, and pgAdmin services.

### Topics
- RAG (Retrieval-Augmented Generation)
- PydanticAI
- PostgreSQL
- pgvector
- Docker
- FastAPI
- OpenAI
- Vector Databases

## Prerequisites
- Python 3.x
- Docker & Docker Compose

## Setting Up the Virtual Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **Linux/MacOS**:
     ```bash
     source venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
Execute the following command to run the main application:
```bash
python main.py
```

## Using Docker

### Running PostgreSQL, pgvector, and pgAdmin using Docker Compose
1. Make sure Docker and Docker Compose are installed.
2. Run the following command to start the services:
   ```bash
   docker-compose up -d
   ```
3. To check the running containers:
   ```bash
   docker ps
   ```
4. To stop the services:
   ```bash
   docker-compose down
   ```

## Accessing pgAdmin
After running Docker Compose, you can access pgAdmin at:
```
http://localhost:5050
```

Use the credentials set in your Docker Compose file to log in.


