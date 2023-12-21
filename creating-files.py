import openpyxl
import os
import re

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()[:255]

def sanitize_directory_name(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()[:255]

# Load the workbook and select the active worksheet
workbook = openpyxl.load_workbook('python-katas-fold.xlsx')
sheet = workbook.active

# Iterate over the rows in the sheet
for row in sheet.iter_rows(min_row=2):  # Assuming first row is header
    name = row[0].value
    description = row[1].value
    solution = row[3].value
    rank = row[2].value

    sanitized_name = sanitize_filename(name)
    sanitized_rank = sanitize_directory_name(rank)

    # Replace /* and */ in description
    description = description.replace('/*', '').replace('*/', '')
    
    os.makedirs(sanitized_rank, exist_ok=True)

    with open(os.path.join(sanitized_rank, f'{sanitized_name}.py'), 'w', encoding='utf-8') as file:
        file.write('\n')
        file.write(f' """ \n{description}\n """ \n\n')
        file.write(solution)

print('Python files created successfully.')