import pdfplumber
import re
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")


def document_extraction(file_path: str) -> str:
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    else:
        raise ValueError("Unsupported file format. Use PDF or TXT.")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=API_KEY,
    temperature=0
)


def clean_json_response(response_text: str) -> str:
    response_text = response_text.strip()
    response_text = re.sub(r"^```json", "", response_text)
    response_text = re.sub(r"^```", "", response_text)
    response_text = re.sub(r"```$", "", response_text)
    return response_text.strip()


def agent_reader(text: str) -> dict:
    prompt = ChatPromptTemplate.from_template("""
persona: You are an FNOL Reader Agent with 10 years of experience.

Task:
Read the FNOL document and extract the required fields.
Return output only in valid JSON format.

Expected JSON format:
{{
   "policy_number": null,
   "policyholder_name": null,
   "date": null,
   "time": null,
   "location": null,
   "description": null,
   "claimant": null,
   "third_parties": null,
   "contact_details": null,
   "asset_type": null,
   "asset_id": null,
   "estimated_damage": null,
   "claim_type": null,
   "attachments": null,
   "initial_estimate": null
}}

FNOL file:
{text}
""")

    chain = prompt | llm
    response = chain.invoke({"text": text})
    output = clean_json_response(response.content)

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        raise ValueError(f"LLM did not return valid JSON.\nResponse was:\n{output}")


def validate_fields(data: dict) -> list:
    mandatory_fields = [
        "policy_number",
        "claim_type",
        "estimated_damage",
        "date",
        "location"
    ]

    missing_fields = [
        field for field in mandatory_fields
        if data.get(field) is None or str(data.get(field)).strip() == ""
    ]
    return missing_fields


def extract_numeric_value(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    match = re.search(r"[\d,]+(?:\.\d+)?", str(value))
    if match:
        return float(match.group(0).replace(",", ""))

    return None


def route_claim(data, missing_field):
    if missing_field:
        return "Manual Review", "Mandatory fields are missing"

    description = (data.get("description") or "").lower()
    claim_type = (data.get("claim_type") or "").lower()
    estimated_damage = extract_numeric_value(data.get("estimated_damage"))

    fraud = ["fraud", "inconsistent", "staged"]

    if any(word in description for word in fraud):
        return "Investigation Flag", "Suspicious keywords found in description"

    if claim_type == "injury":
        return "Specialist Queue", "Claim type is injury"

    if estimated_damage is not None and estimated_damage < 25000:
        return "Fast-track", "Estimated damage is below 25,000"

    return "Standard Review", "No special routing condition matched"


def main():
    file_path = input("Enter the FNOL file path (.pdf or .txt): ").strip()

    try:
        text = document_extraction(file_path)

        if not text.strip():
            print("No text could be extracted from the file.")
            return

        data = agent_reader(text)
        missing = validate_fields(data)
        recommended_route, reasoning = route_claim(data, missing)

        final_output = {
            "extracted_data": data,
            "missing_fields": missing,
            "recommended_route": recommended_route,
            "reasoning": reasoning
        }

        print(json.dumps(final_output, indent=4))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()