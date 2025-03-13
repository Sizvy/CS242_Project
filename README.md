# CS242 Project: StackOverflow Search Engine

Welcome to the **CS242 Project** repository! This project is an AI-powered search engine designed to help developers quickly find solutions to programming errors by leveraging **Stack Overflow** data. The system combines **keyword-based search** (using Lucene) and **semantic search** (using BERT) to retrieve relevant answers, and it employs a **Large Language Model (LLM)** to generate concise and accurate solutions.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Team](#team)

## Overview
This project aims to streamline the process of finding solutions to programming errors by:
1. **Scraping and indexing** error-related questions and answers from Stack Overflow.
2. Providing **two search methods**:
   - **Keyword-based search** using **Lucene**.
   - **Semantic search** using **BERT** and **FAISS** for dense retrieval.
3. Generating **AI-powered solutions** using a **Large Language Model (LLM)**.

The system is backed by a **user-friendly web interface** that allows users to enter queries, view ranked solutions, and read AI-generated summaries.

## Features
- **Dual Search Modes**: Choose between **Lucene** (keyword-based) and **BERT** (semantic) search.
- **AI-Powered Solutions**: The system uses **Qwen 2.5 3B Instruct** (via Hugging Face API) to generate concise and accurate answers.
- **Interactive GUI**: A Flask-based web interface for real-time query processing and result display.
- **Efficient Retrieval**: Combines **Lucene**, **BERT**, and **FAISS** for fast and accurate document retrieval.
- **Live Demo**: Try out the system in real-time using the provided link.

## Technologies Used
- **Web Scraping**: Scrapy (for collecting Stack Overflow data).
- **Indexing and Search**:
  - **Sparse Retrieval**: Pylucene (Inverted Index, Vector Space Model, Okapi BM25).
  - **Dense Retrieval**: BERT (🤗 Transformers) and FAISS for semantic search.
- **Large Language Model**: Qwen 2.5 3B Instruct (via Hugging Face API).
- **Backend**: Flask API for connecting search and AI models.
- **Frontend**: HTML, CSS, JavaScript for the user interface.
- **Deployment**: Hosted on a live server for real-time access.

## How It Works
1. **Data Collection**: Error-related questions, answers, tags, and comments are scraped from Stack Overflow using Scrapy.
2. **Indexing**:
   - **Lucene**: Creates an inverted index for fast keyword-based retrieval.
   - **BERT**: Transforms text into contextualized embeddings for semantic search.
3. **Search**:
   - The user enters a query (e.g., a programming error).
   - The system retrieves the top-k relevant documents using either Lucene or BERT.
4. **LLM Integration**:
   - The query and retrieved documents are sent to the LLM (Qwen 2.5 3B Instruct) via the Hugging Face API.
   - The LLM generates a solution, which is displayed in the GUI.
5. **Result Display**: The user sees ranked solutions with AI-generated summaries.

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sizvy/CS242_Project.git
   cd CS242_Project
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Add your Hugging face API key**:
   ```bash
   HUGGING_FACE_API_KEY=your_api_key_here
4. **Run the flask application**:
   ```bash
   python3 app.py
5. **Access the GUI**:
   ```bash
   Open your browser and navigate to http://localhost:8080.
## Usage
1. Enter your query (e.g., a programming error) in the search bar.
2. Choose between Lucene (keyword-based) or BERT (semantic) search.
3. View the ranked results and AI-generated summaries.
4. Click on any result to see more details.
   
## Team
This project was developed by Team 06 as part of the CS242 Course (Winter 2025). Team members:
**G M Shahariar**
**Md Taukir Azam Chowdhury**
**Md. Olid Bhuiyan**
**Samiha Khan**
**Zabir Al Nazi**
   
