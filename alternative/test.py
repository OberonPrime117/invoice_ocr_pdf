import re
import json

text = """[Your provided text goes here]"""

# Define a regular expression pattern to extract the required information
pattern = r'FSSAI_\s*=\s*:\s*(\d+)\n'
pattern += r'PAN NO\s*:\s*(\w+)\n'
pattern += r'TAN NO\s*:\s*(\w+)\n'

# Use regular expressions to find matches in the text
matches = re.findall(pattern, text)

# Create a dictionary with the extracted information
data = {
    "FSSAI": matches[0][0],
    "PAN NO": matches[1][0],
    "TAN NO": matches[2][0]
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data, indent=4)

# Print the JSON data
print(json_data)
