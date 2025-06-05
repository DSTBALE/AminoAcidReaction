#!/usr/bin/env python3
"""
Script to enhance the existing JSON file with detailed reaction conditions
from the cleaned text file.
"""

import json
import re
import sys

def parse_reaction_conditions(text_content):
    """
    Parse the cleaned text file and extract reaction conditions.
    Returns a dictionary with CAS numbers as keys.
    """
    
    reactions = {}
    
    # Split content into sections by CAS Reaction Number
    cas_pattern = r'CAS Reaction Number: ([\d-]+CAS-[\d]+)'
    sections = re.split(cas_pattern, text_content)
    
    # Process each section (skip first empty section)
    for i in range(1, len(sections), 2):
        cas_number = sections[i]
        section_content = sections[i + 1] if i + 1 < len(sections) else ""
        
        reaction_data = {
            'solvents': [],
            'catalysts': [],
            'reagents': [],
            'conditions': []
        }
        
        lines = section_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Parse different types of information
            if 'Solvents:' in line:
                solvents_info = extract_solvents(line)
                if solvents_info:
                    reaction_data['solvents'].extend(solvents_info)
                    
            elif 'Catalysts:' in line:
                catalysts_info = extract_catalysts(line)
                if catalysts_info:
                    reaction_data['catalysts'].extend(catalysts_info)
                    
            elif 'Reagents:' in line:
                reagents_info = extract_reagents(line)
                if reagents_info:
                    reaction_data['reagents'].extend(reagents_info)
            
            # Extract general conditions (temperature, time, pressure, pH)
            conditions = extract_conditions(line)
            if conditions:
                reaction_data['conditions'].extend(conditions)
        
        reactions[cas_number] = reaction_data
    
    return reactions

def extract_solvents(line):
    """Extract solvent information from a line."""
    solvents = []
    
    # Find the solvents part
    match = re.search(r'Solvents:\s*([^|;]+)', line)
    if match:
        solvents_text = match.group(1).strip()
        
        # Split by comma to get individual solvents
        solvent_names = [s.strip() for s in solvents_text.split(',')]
        
        for solvent in solvent_names:
            if solvent:
                solvents.append({
                    'name': solvent,
                    'conditions': extract_conditions_from_text(line)
                })
    
    return solvents

def extract_catalysts(line):
    """Extract catalyst information from a line."""
    catalysts = []
    
    # Find the catalysts part
    match = re.search(r'Catalysts:\s*([^|;]+)', line)
    if match:
        catalysts_text = match.group(1).strip()
        
        # Split by comma to get individual catalysts
        catalyst_names = [c.strip() for c in catalysts_text.split(',')]
        
        for catalyst in catalyst_names:
            if catalyst:
                catalysts.append({
                    'name': catalyst,
                    'conditions': extract_conditions_from_text(line)
                })
    
    return catalysts

def extract_reagents(line):
    """Extract reagent information from a line."""
    reagents = []
    
    # Find the reagents part
    match = re.search(r'Reagents:\s*([^|;]+)', line)
    if match:
        reagents_text = match.group(1).strip()
        
        # Split by comma to get individual reagents
        reagent_names = [r.strip() for r in reagents_text.split(',')]
        
        for reagent in reagent_names:
            if reagent:
                reagents.append({
                    'name': reagent,
                    'conditions': extract_conditions_from_text(line)
                })
    
    return reagents

def extract_conditions_from_text(text):
    """Extract conditions (temperature, time, pressure, pH) from text."""
    conditions = {}
    
    # Temperature patterns (only numeric temperatures and reflux)
    temp_patterns = [
        (r'(\d+(?:\.\d+)?)\s*°C', 'numeric'),
        (r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*°C', 'range'),
        (r'\brt\b', 'rt'),
        (r'\breflux\b', 'reflux')
    ]
    
    for pattern, pattern_type in temp_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            if pattern_type == 'rt':
                conditions['temperature'] = 'room temperature'
            elif pattern_type == 'reflux':
                conditions['temperature'] = 'reflux'
            elif pattern_type == 'range':
                conditions['temperature'] = f"{matches[0][0]}-{matches[0][1]}°C"
            elif pattern_type == 'numeric':
                conditions['temperature'] = f"{matches[0]}°C"
    
    # Time patterns
    time_patterns = [
        (r'(\d+(?:\.\d+)?)\s*h\b', 'hours'),
        (r'(\d+(?:\.\d+)?)\s*min\b', 'minutes'),
        (r'(\d+(?:\.\d+)?)\s*d\b', 'days'),
        (r'\bovernight\b', 'overnight')
    ]
    
    for pattern, unit in time_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            if unit == 'overnight':
                conditions['time'] = 'overnight'
            else:
                conditions['time'] = f"{matches[0]} {unit}"
    
    # Pressure patterns
    pressure_patterns = [
        (r'(\d+(?:\.\d+)?)\s*MPa\b', 'MPa'),
        (r'(\d+(?:\.\d+)?)\s*kPa\b', 'kPa'),
        (r'(\d+(?:\.\d+)?)\s*atm\b', 'atm'),
        (r'(\d+(?:\.\d+)?)\s*bar\b', 'bar'),
        (r'(\d+(?:\.\d+)?)\s*psi\b', 'psi')
    ]
    
    for pattern, unit in pressure_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            conditions['pressure'] = f"{matches[0]} {unit}"
    
    # pH patterns
    ph_matches = re.findall(r'pH\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if ph_matches:
        conditions['pH'] = ph_matches[0]
    
    # Other conditions (cooled, heated, neutralized, etc.)
    other_conditions = []
    other_patterns = [
        r'\bcooled\b',
        r'\bheated\b',
        r'\bneutralized\b',
        r'\bstirred\b',
        r'\bfiltered\b',
        r'\bwashed\b',
        r'\bdried\b',
        r'\bevaporated\b',
        r'\bconcentrated\b',
        r'\bcrystallized\b',
        r'\brecrystallized\b',
        r'\bpurified\b'
    ]
    
    for pattern in other_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Remove 'b' from pattern and add to other conditions
            condition_name = pattern.replace('\\b', '').replace('\\', '')
            if condition_name not in other_conditions:
                other_conditions.append(condition_name)
    
    if other_conditions:
        conditions['other'] = other_conditions
    
    return conditions

def extract_conditions(line):
    """Extract general conditions from any line."""
    conditions = []
    
    # Extract all conditions from the line
    condition_data = extract_conditions_from_text(line)
    if condition_data:
        conditions.append(condition_data)
    
    return conditions

def enhance_json_with_conditions(json_file, text_file, output_file):
    """
    Enhance the existing JSON file with conditions from the text file.
    """
    
    # Read the existing JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Read the text file
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    # Parse reaction conditions from text
    reaction_conditions = parse_reaction_conditions(text_content)
    
    # Enhance JSON data
    enhanced_count = 0
    
    for reaction_key, reaction_data in json_data.items():
        cas_number = reaction_data.get('reaction_number')
        
        if cas_number in reaction_conditions:
            conditions_data = reaction_conditions[cas_number]
            
            # Add detailed solvent information
            if conditions_data['solvents'] and 'solvents' in reaction_data:
                for i, solvent in enumerate(reaction_data['solvents']):
                    if i < len(conditions_data['solvents']):
                        solvent['name'] = conditions_data['solvents'][i]['name']
                        solvent['conditions'] = conditions_data['solvents'][i]['conditions']
            
            # Add catalyst information if not present
            if conditions_data['catalysts']:
                if 'catalysts' not in reaction_data:
                    reaction_data['catalysts'] = []
                
                for catalyst_info in conditions_data['catalysts']:
                    reaction_data['catalysts'].append({
                        'name': catalyst_info['name'],
                        'conditions': catalyst_info['conditions']
                    })
            
            # Add detailed reagent information
            if conditions_data['reagents'] and 'reagents' in reaction_data:
                for i, reagent in enumerate(reaction_data['reagents']):
                    if i < len(conditions_data['reagents']):
                        reagent['name'] = conditions_data['reagents'][i]['name']
                        reagent['conditions'] = conditions_data['reagents'][i]['conditions']
            
            # Add general reaction conditions
            if conditions_data['conditions']:
                reaction_data['reaction_conditions'] = conditions_data['conditions']
            
            enhanced_count += 1
    
    # Write enhanced JSON to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"Enhanced {enhanced_count} reactions with detailed conditions")
    print(f"Enhanced JSON saved to: {output_file}")

def main():
    json_file = "Valine/valine_reactions.json"
    text_file = "Valine/combine_cleaned.txt"
    output_file = ("Valine/valine_reactions_new.json")
    
    print("Enhancing JSON file with reaction conditions...")
    print(f"Reading JSON from: {json_file}")
    print(f"Reading conditions from: {text_file}")
    
    enhance_json_with_conditions(json_file, text_file, output_file)
    
    print("\nEnhancement completed!")
    print("Added information:")
    print("- Detailed solvent names and conditions")
    print("- Catalyst names and conditions")
    print("- Reagent names and conditions")
    print("- Reaction conditions (temperature, time, pressure, pH)")

if __name__ == "__main__":
    main() 