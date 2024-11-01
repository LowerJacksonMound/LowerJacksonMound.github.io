import json
import re

# File paths
input_file = "dictionary.json"  # Your current output with all acronyms on one line
output_file = "formatted_dictionary.json"  # Reformatted output

# Read the single-line dictionary content
with open(input_file, "r") as file:
    content = file.read()

# Regular expression to match acronyms and definitions
# This assumes each acronym-definition pair is separated by a colon and has some spaces after it
matches = re.findall(r'(\b[A-Z]{2,}\b):\s*([^:]+)', content)

# Convert matches to a dictionary format
acronym_dict = {acronym.strip(): definition.strip() for acronym, definition in matches}

# Write to a properly formatted JSON file
with open(output_file, "w") as json_file:
    json.dump(acronym_dict, json_file, indent=4)

print(f"Reformatted dictionary saved to {output_file}.")
