import re, json
from typing import List
from pathlib import Path

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"[^\w\s.,!?-]", "", text).strip()

def extract_emails(text: str) -> List[str]:
    return re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)

def extract_phone_numbers(text: str) -> List[str]:
    return re.findall(r"\+?\d[\d -]{8,}\d", text)

def save_json(data, path: Path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
