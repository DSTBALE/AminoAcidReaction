#!/usr/bin/env python3
"""
Script to filter out reactions containing "reflux" from combine_cleaned.txt
Keeps only reactions that do NOT contain "reflux" anywhere in their text.
"""

import re
import os

def filter_reactions_without_reflux(input_file, output_file):
    """
    Read the input file, filter out reactions containing 'reflux', 
    and write the remaining reactions to the output file.
    """
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Split content into individual reactions
    # Each reaction starts with "CAS Reaction Number:"
    reactions = re.split(r'(?=CAS Reaction Number:)', content)
    
    # Remove empty first element if it exists
    if reactions and not reactions[0].strip():
        reactions = reactions[1:]
    
    # Filter out reactions containing "reflux" (case-insensitive)
    filtered_reactions = []
    reflux_count = 0
    total_count = len(reactions)
    
    for reaction in reactions:
        if 'reflux' not in reaction.lower():
            filtered_reactions.append(reaction)
        else:
            reflux_count += 1
    
    # Write filtered reactions to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for reaction in filtered_reactions:
                f.write(reaction)
                if not reaction.endswith('\n'):
                    f.write('\n')
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return
    
    # Print statistics
    print(f"Processing complete!")
    print(f"Total reactions found: {total_count}")
    print(f"Reactions with 'reflux': {reflux_count}")
    print(f"Reactions without 'reflux': {len(filtered_reactions)}")
    print(f"Filtered data saved to: {output_file}")

def main():
    # File paths
    input_file = "Asparagine/combine_cleaned.txt"
    output_file = "Asparagine/combine_cleaned_no_reflux.txt"
    
    print("Filtering reactions without 'reflux'...")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("-" * 50)
    
    filter_reactions_without_reflux(input_file, output_file)

if __name__ == "__main__":
    main() 