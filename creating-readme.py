import openpyxl
import urllib.parse
import os
import re

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()[:255]

def sanitize_directory_name(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()[:255]

def format_markdown_link(name, rank):
    # URL encoding for special characters and whitespaces
    encoded_name = urllib.parse.quote(name)
    encoded_rank = urllib.parse.quote(rank)
    return f'1. [{name}](https://github.com/YOUR_NIKNAME_HERE/codewars/blob/main/Python/{encoded_rank}/{encoded_name}.py)'

# Load the workbook and select the active worksheet
workbook = openpyxl.load_workbook('python-katas-fold.xlsx')
sheet = workbook.active

# List to store formatted markdown links
markdown_links = []

# Iterate over the rows in the sheet
for row in sheet.iter_rows(min_row=2):  # Assuming first row is header
    name = row[0].value or ''  # Replace None with empty string
    rank = row[2].value or ''  # Replace None with empty string
    
    # Sanitize name and rank
    sanitized_name = sanitize_filename(name)
    sanitized_rank = sanitize_directory_name(rank)

    # Format and store the markdown link
    markdown_links.append(format_markdown_link(sanitized_name, sanitized_rank))

# Write to README.md file
with open('README.md', 'w', encoding='utf-8') as file:
    file.write('\n'.join(markdown_links))

print('README.md file created successfully.')