from striprtf.striprtf import rtf_to_text

directory = ["Aspartate", "Cysteine", "Glutamate", "Glutamine", "Glycine", "Histidine", "Lysine",
             "Phenylalanine", "Proline", "Serine"]

for name in directory:
    # 1. Read the RTF file
    with open(f'{name}/combine.rtf', 'r', encoding='utf-8') as rtf_file:
        rtf_content = rtf_file.read()

    # 2. Convert RTF to plain text
    plain_text = rtf_to_text(rtf_content)

    # 3. Write the result to a .txt file
    with open(f'{name}/combine.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(plain_text)

print("Conversion complete: 'combine.txt's are all written.")