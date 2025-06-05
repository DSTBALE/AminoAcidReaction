#!/usr/bin/env python3
"""
Script to edit the original combine.txt file by removing unwanted lines.
Keeps only: CAS Reaction Number, Solvents, Catalysts, Reagents, and conditions.
"""

import re
import os

def edit_combine_file(input_file):
    """
    Edit the original combine.txt file to keep only relevant information.
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into sections by CAS Reaction Number
    cas_pattern = r'CAS Reaction Number: ([\d-]+CAS-[\d]+)'
    sections = re.split(cas_pattern, content)
    
    cleaned_content = []
    
    # Process each section (skip first empty section)
    for i in range(1, len(sections), 2):
        cas_number = sections[i]
        section_content = sections[i + 1] if i + 1 < len(sections) else ""
        
        # Extract reaction steps data
        step_lines = []
        lines = section_content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for step lines that contain reaction conditions
            # Pattern 1: Lines starting with numbered steps like "1.1|"
            if re.match(r'^\d+\.\d+\|', line):
                # Check if line contains relevant information
                relevant_keywords = [
                    'Solvents:', 'Catalysts:', 'Reagents:', 
                    '°C', 'pressure', 'pH', 'atm', 'bar', 'psi', 'MPa', 'kPa',
                    'min', 'h', 'd', 'rt', 'reflux', 'cooled', 'heated'
                ]
                
                if any(keyword in line for keyword in relevant_keywords):
                    step_lines.append(line)
            
            # Pattern 2: Lines starting with just "|" followed by relevant keywords
            elif re.match(r'^\|', line):
                relevant_keywords = [
                    'Solvents:', 'Catalysts:', 'Reagents:'
                ]
                
                if any(keyword in line for keyword in relevant_keywords):
                    step_lines.append(line)
        
        if step_lines:
            cleaned_content.append(f"CAS Reaction Number: {cas_number}")
            for step_line in step_lines:
                cleaned_content.append(step_line)
            cleaned_content.append("")  # Add blank line between reactions
    
    # Write cleaned content back to the original file
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_content))
    
    print(f"File edited: {input_file}")
    print(f"Kept {len([line for line in cleaned_content if line.startswith('CAS Reaction Number:')])} reactions")

def main():
    input_file = ("Tyrosine/combine.txt")
    
    print("Editing the original file...")
    print("This will remove all unwanted lines and keep only essential reaction information.")
    print("Now includes support for lines starting with '|' that contain Solvents, Catalysts, or Reagents.")
    
    # Create a new output file instead of overwriting
    output_file = input_file.replace('.txt', '_cleaned.txt')
    
    # Copy the original to the output file first
    with open(input_file, 'r', encoding='utf-8') as src, open(output_file, 'w', encoding='utf-8') as dst:
        dst.write(src.read())
    
    edit_combine_file(output_file)

if __name__ == "__main__":
    main() 