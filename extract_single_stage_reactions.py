#!/usr/bin/env python3
"""
Script to extract reactions with only one stage from asparagine_reactions.json
and save them to a new JSON file with continuous numbering.
"""

import json
import os

def extract_single_stage_reactions(input_file, output_file):
    """
    Extract reactions with stages = 1 from the input JSON file
    and save them to a new JSON file with continuous numbering.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to the output JSON file
    """
    try:
        # Read the input JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filter reactions with stages = 1 and renumber continuously
        single_stage_reactions = {}
        reaction_counter = 1
        
        for reaction_key, reaction_data in data.items():
            if reaction_data.get('stages') == 1:
                # Create new continuous key
                new_key = f"reaction{reaction_counter}"
                single_stage_reactions[new_key] = reaction_data
                reaction_counter += 1
        
        # Save the filtered reactions to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(single_stage_reactions, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully extracted {len(single_stage_reactions)} reactions with 1 stage")
        print(f"Original file had {len(data)} total reactions")
        print(f"Reactions renumbered continuously from reaction1 to reaction{len(single_stage_reactions)}")
        print(f"Single-stage reactions saved to: {output_file}")
        
        return single_stage_reactions
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    # Define file paths
    input_file = "Asparagine/asparagine_reactions.json"
    output_file = "Asparagine/single_stage_reactions.json"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        print("Please make sure the file path is correct.")
        return
    
    # Extract single-stage reactions
    result = extract_single_stage_reactions(input_file, output_file)
    
    if result is not None:
        print("\nExtraction completed successfully!")
    else:
        print("\nExtraction failed!")

if __name__ == "__main__":
    main() 