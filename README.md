# FNOL Document Extraction and Claim Routing System

This project is an AI-powered insurance workflow automation system that processes **FNOL (First Notice of Loss)** documents and recommends the appropriate claim routing path.

The system supports **PDF and TXT files**, extracts claim-related information using **Google Gemini**, validates mandatory fields, and routes the claim using predefined business logic.

---

## Project Overview

In insurance claim processing, FNOL documents often contain important details such as policy number, date of incident, location, claim type, estimated damage, and more.

This project automates that workflow in four main steps:

1. Extract text from PDF or TXT files
2. Use an LLM to convert unstructured text into structured JSON
3. Validate required fields
4. Route the claim to the correct review path

---

## Features

- Supports **PDF** and **TXT** input files
- Extracts text using `pdfplumber`
- Uses **Gemini 2.5 Flash** for structured data extraction
- Returns claim data in valid **JSON format**
- Validates mandatory claim fields
- Applies **rule-based routing logic**
- Handles missing data and suspicious claim descriptions
- Combines **GenAI + business rules** in one workflow

---

## Workflow

### 1. Document Extraction
The system reads the FNOL file and extracts text.

Supported formats:
- `.pdf`
- `.txt`

### 2. Reader Agent
A Gemini-powered agent reads the extracted FNOL content and returns structured claim data in JSON format.

### 3. Validation
The extracted data is checked for mandatory fields such as:
- `policy_number`
- `claim_type`
- `estimated_damage`
- `date`
- `location`

### 4. Claim Routing
The system recommends one of the following routes:

- **Manual Review** → if required fields are missing
- **Investigation Flag** → if suspicious keywords are found
- **Specialist Queue** → if claim type is injury
- **Fast-track** → if estimated damage is below 25,000
- **Standard Review** → default path

---

## Tech Stack

- Python
- Google Gemini 2.5 Flash
- LangChain
- pdfplumber
- python-dotenv
- JSON
- Regex

---

## Project Structure

```bash
project-folder/
│
├── app.py
├── .env
├── requirements.txt
├── sample_data/
│   ├── fnol_sample.txt
│   └── fnol_sample.pdf
└── README.md
