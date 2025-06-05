# rtf_to_txt.py
from striprtf.striprtf import rtf_to_text

# 1. Read the RTF file
with open('Tyrosine/combine.rtf', 'r', encoding='utf-8') as rtf_file:
    rtf_content = rtf_file.read()

# 2. Convert RTF to plain text
plain_text = rtf_to_text(rtf_content)

# 3. Write the result to a .txt file
with open('Tyrosine/combine.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(plain_text)

print("Conversion complete: 'combine.txt' written.")