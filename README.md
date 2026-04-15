# FNOL Document Extraction and Claim Routing System

An AI-powered insurance workflow automation project that processes **FNOL (First Notice of Loss)** documents, extracts structured claim information using **Google Gemini**, validates mandatory fields, and recommends a routing path using rule-based logic.

---

## Project Overview

This project is designed to simulate an insurance claim intake workflow.

It accepts an FNOL document in **PDF** or **TXT** format, extracts the text content, sends it to a Gemini-powered extraction agent, validates the returned fields, and then routes the claim to the appropriate queue based on predefined business rules.

This project demonstrates the practical use of:

- **Document extraction**
- **LLM-based JSON field extraction**
- **Validation of critical business fields**
- **Rule-based claim routing**

---

## Approach

The system follows a simple 4-step pipeline:

### 1. Document Extraction
- If the input file is a `.txt` file, the system reads it directly.
- If the input file is a `.pdf` file, the system uses `pdfplumber` to extract text page by page.
- If the format is unsupported, the system raises an error.

### 2. AI-Based Field Extraction
- The extracted FNOL text is passed to **Google Gemini 2.5 Flash** through LangChain.
- The model is instructed to return only valid JSON.
- The expected fields include policy number, date, location, claim type, estimated damage, and more.

### 3. Validation
The system checks whether these mandatory fields are present:

- `policy_number`
- `claim_type`
- `estimated_damage`
- `date`
- `location`

If any of these are missing, the claim is marked for **Manual Review**.

### 4. Claim Routing
The system recommends a route based on business rules:

- **Manual Review** → if mandatory fields are missing
- **Investigation Flag** → if suspicious keywords like `fraud`, `inconsistent`, or `staged` appear
- **Specialist Queue** → if the claim type is `injury`
- **Fast-track** → if estimated damage is below 25,000
- **Standard Review** → if no special condition applies

---

## Features

- Supports **PDF** and **TXT** input files
- Extracts text using `pdfplumber`
- Uses **Gemini 2.5 Flash** for structured JSON extraction
- Cleans model output before parsing JSON
- Validates mandatory claim fields
- Routes claims using predefined business logic
- Handles extraction and input errors

---

## Tech Stack

- Python
- LangChain
- Google Gemini 2.5 Flash
- pdfplumber
- python-dotenv
- JSON
- Regex

---

## Repository Structure

```bash
Fnol-document-extraction-and-routing/
│
├── FNOL_extraction_project.py
├── Requirement.txt
└── README.md

▶️ Steps to Run (Windows)

git clone https://github.com/HARIHARANG7225/Fnol-document-extraction-and-routing.git
cd Fnol-document-extraction-and-routing
python -m venv venv
venv\Scripts\activate
pip install -r Requirement.txt

Create a .env file in the project root and add:

GOOGLE_API_KEY=your_google_api_key_here

Make sure your input file is ready (example: sample.txt or sample.pdf)

python FNOL_extraction_project.py

When prompted, enter:

Enter the FNOL file path (.pdf or .txt): sample.txt
