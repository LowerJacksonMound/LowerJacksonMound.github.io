import pdfplumber
import json
import re
import os
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# Keywords or patterns to exclude (adjust based on your PDFs)
EXCLUSION_PATTERNS = [
    r'\bIntroduction\b',           # Section headers
    r'\bDocument Description\b',
    r'\bPage\s+\d+\b'              # Page numbers (e.g., "Page 12")
]

# Updated regex pattern to capture different separators and handle line breaks
# This pattern captures an acronym followed by a separator and then its definition.
# It ensures that the definition ends at a line break or another acronym.
ACRONYM_PATTERN = re.compile(
    r'\b([A-Z]{2,})\b\s*[-–—:|]\s*(.*?)\b(?=[A-Z]{2,}\b\s*[-–—:|]|$)',
    re.DOTALL
)

def clean_text(text):
    """Remove unwanted sections from the text based on exclusion patterns."""
    for pattern in EXCLUSION_PATTERNS:
        # Remove entire lines containing the exclusion patterns
        text = re.sub(rf'.*{pattern}.*\n?', '', text, flags=re.IGNORECASE)
    return text

def extract_acronyms_from_text(text):
    """Extract acronyms and definitions from cleaned text."""
    acronyms = defaultdict(set)  # Use a set to store multiple definitions per acronym
    matches = ACRONYM_PATTERN.findall(text)
    for acronym, definition in matches:
        # Clean up whitespace and line breaks within definitions
        clean_def = ' '.join(definition.strip().split())
        acronyms[acronym].add(clean_def)
    return acronyms

def process_pdf_file(pdf_path):
    """Extract text, clean it, and then find acronym-definition pairs."""
    all_text = ""
    missed_pages = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    # Join lines to handle acronyms and definitions split across lines
                    all_text += ' '.join(text.splitlines()) + "\n"
                    logging.info(f"Processed page {page_num} of {pdf_path}")
                else:
                    missed_pages.append(page_num)
                    logging.warning(f"No text extracted from page {page_num} of {pdf_path}")
    except Exception as e:
        logging.error(f"Failed to process {pdf_path}: {e}")
        return defaultdict(set)  # Return empty if failed

    if missed_pages:
        logging.warning(f"Missed pages in {pdf_path}: {missed_pages}")

    # Clean extraneous text and extract acronyms
    cleaned_text = clean_text(all_text)
    return extract_acronyms_from_text(cleaned_text)

def merge_acronyms(all_acronyms):
    """Merge multiple acronym dictionaries, handling multiple definitions."""
    merged = {}
    for acronym, definitions in all_acronyms.items():
        if len(definitions) == 1:
            merged[acronym] = definitions.pop()
        else:
            merged[acronym] = list(definitions)  # Store multiple definitions as a list
            logging.info(f"Acronym '{acronym}' has multiple definitions.")
    return merged

def main(input_directory='.', output_file="dictionary.json"):
    """Main function to process PDFs and extract acronyms."""
    all_acronyms = defaultdict(set)
    pdf_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.pdf')]

    if not pdf_files:
        logging.warning("No PDF files found in the specified directory.")
        return

    for filename in pdf_files:
        pdf_path = os.path.join(input_directory, filename)
        logging.info(f"Processing {filename}...")
        acronyms = process_pdf_file(pdf_path)
        for acronym, defs in acronyms.items():
            all_acronyms[acronym].update(defs)

    merged_acronyms = merge_acronyms(all_acronyms)

    # Check if output file exists to backup
    if os.path.exists(output_file):
        backup_file = f"{output_file}.backup"
        try:
            os.rename(output_file, backup_file)
            logging.info(f"Existing '{output_file}' backed up as '{backup_file}'.")
        except Exception as e:
            logging.error(f"Failed to backup existing '{output_file}': {e}")
            return

    # Save all extracted acronyms to dictionary.json
    try:
        with open(output_file, "w", encoding='utf-8') as json_file:
            json.dump(merged_acronyms, json_file, indent=4, ensure_ascii=False)
        logging.info(f"Acronyms extracted and saved to '{output_file}'.")
    except Exception as e:
        logging.error(f"Failed to write to '{output_file}': {e}")

if __name__ == "__main__":
    main()
