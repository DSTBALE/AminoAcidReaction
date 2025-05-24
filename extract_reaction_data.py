#!/usr/bin/env python3
import json
import re

def extract_reaction_data(file_path):
    """Extract reaction data from the given file and convert to JSON format."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Split into reactions - each reaction starts with $RXN and ends before the next $RXN
    reaction_blocks = re.split(r'\$RFMT \$RIREG SCHEME\d+ STEP\d+\s+\$RXN', content)
    
    if not reaction_blocks:
        return {}
    
    reactions = {}
    reaction_count = 0
    
    # Process each reaction block
    for block in reaction_blocks:
        if not block.strip():
            continue
        
        # Check if this is a valid reaction block (has $MOL in it)
        if "$MOL" in block:
            reaction_count += 1
            reaction_data = parse_reaction_block(block)
            if reaction_data:
                reactions[f"reaction{reaction_count}"] = reaction_data
    
    return reactions

def parse_reaction_block(block):
    """Parse a single reaction block to extract relevant data."""
    # Extract compound sections
    mol_sections = []
    
    # Get all sections between $MOL and the next $MOL or end
    mol_matches = re.finditer(r'\$MOL(.*?)(?=\$MOL|\Z)', block, re.DOTALL)
    for match in mol_matches:
        mol_section = match.group(1).strip()
        if mol_section:
            lines = mol_section.split('\n')
            name = lines[0].strip() if lines[0].strip() else ""
            formula = lines[1].strip() if len(lines) > 1 else ""
            mol_sections.append({
                "name": name,
                "formula": formula
            })
    
    # Extract reaction metadata
    reaction_data = {}
    
    # Extract reaction number
    rxn_number_match = re.search(r'\$DTYPE RXN:VAR\(1\):CAS_Reaction_Number\s+\$DATUM ([\w-]+)', block)
    if rxn_number_match:
        reaction_data["reaction_number"] = rxn_number_match.group(1)
    
    # Extract steps
    steps_match = re.search(r'\$DTYPE RXN:VAR\(1\):STEPS\s+\$DATUM (\d+)', block)
    if steps_match:
        reaction_data["steps"] = int(steps_match.group(1))
    
    # Extract stages
    stages_match = re.search(r'\$DTYPE RXN:VAR\(1\):STAGES\s+\$DATUM (\d+)', block)
    if stages_match:
        reaction_data["stages"] = int(stages_match.group(1))
    
    # Process reactants
    reactants = []
    rct_matches = re.finditer(r'\$DTYPE RXN:RCT\((\d+)\):CAS_RN\s+\$DATUM (\d+-\d+-\d+)', block)
    for match in rct_matches:
        idx = int(match.group(1)) - 1  # Convert to 0-indexed
        cas_rn = match.group(2)
        if idx < len(mol_sections):
            reactant = mol_sections[idx].copy()
            reactant["cas_rn"] = cas_rn
            reactants.append(reactant)
    
    # Process products
    products = []
    pro_matches = re.finditer(r'\$DTYPE RXN:PRO\((\d+)\):CAS_RN\s+\$DATUM (\d+-\d+-\d+)', block)
    for match in pro_matches:
        idx = int(match.group(1)) - 1  # Convert to 0-indexed
        # Offset index by number of reactants to get the right position in mol_sections
        idx_in_mol = len(reactants) + idx
        cas_rn = match.group(2)
        if idx_in_mol < len(mol_sections):
            product = mol_sections[idx_in_mol].copy()
            product["cas_rn"] = cas_rn
            products.append(product)
    
    # Process reagents
    reagents = []
    rgt_matches = re.finditer(r'\$DTYPE RXN:VAR\(1\):RGT\((\d+)\):CAS_RN\s+\$DATUM (\d+-\d+-\d+)', block)
    for match in rgt_matches:
        cas_rn = match.group(2)
        reagents.append({"cas_rn": cas_rn})
    
    # Process solvents
    solvents = []
    sol_matches = re.finditer(r'\$DTYPE RXN:VAR\(1\):SOL\((\d+)\):CAS_RN\s+\$DATUM (\d+-\d+-\d+)', block)
    for match in sol_matches:
        cas_rn = match.group(2)
        solvents.append({"cas_rn": cas_rn})
    
    # Process catalysts
    catalysts = []
    cat_matches = re.finditer(r'\$DTYPE RXN:VAR\(1\):CAT\((\d+)\):CAS_RN\s+\$DATUM (\d+-\d+-\d+)', block)
    for match in cat_matches:
        cas_rn = match.group(2)
        catalysts.append({"cas_rn": cas_rn})
    
    # Set reactants in the reaction data
    if len(reactants) == 1:
        reaction_data["reactant"] = reactants[0]
    elif len(reactants) > 1:
        reaction_data["reactants"] = reactants
    
    # Set products in the reaction data
    if len(products) == 1:
        reaction_data["product"] = products[0]
    elif len(products) > 1:
        reaction_data["products"] = products
    
    # Add other components if present
    if reagents:
        reaction_data["reagents"] = reagents
    
    if solvents:
        reaction_data["solvents"] = solvents
        
    if catalysts:
        reaction_data["catalysts"] = catalysts
    
    # Extract notes if available
    notes_match = re.search(r'\$DTYPE RXN:VAR\(1\):NOTES\s+\$DATUM (.*?)(?=\$)', block, re.DOTALL)
    if notes_match:
        notes = notes_match.group(1).strip()
        if notes:
            reaction_data["notes"] = notes
    
    # Extract conditions if available
    conditions = {}
    
    # Look for common condition parameters
    temp_match = re.search(r'(?:temperature|temp)(?:[: ]+)([-\d]+(?:[ ]?[°CFK])?)', block, re.IGNORECASE)
    if temp_match:
        conditions["temperature"] = temp_match.group(1).strip()
    
    time_match = re.search(r'(?:time|duration)(?:[: ]+)([\d.]+(?:[ ]?[hmsd])?)', block, re.IGNORECASE)
    if time_match:
        conditions["time"] = time_match.group(1).strip()
    
    pressure_match = re.search(r'(?:pressure)(?:[: ]+)([\d.]+(?:[ ]?[a-zA-Z]+)?)', block, re.IGNORECASE)
    if pressure_match:
        conditions["pressure"] = pressure_match.group(1).strip()
    
    if conditions:
        reaction_data["conditions"] = conditions
    
    # Extract reference title if available
    ref_title_match = re.search(r'\$DTYPE RXN:VAR\(1\):REFERENCE\(1\):TITLE\s+\$DATUM (.*?)(?=\$)', block, re.DOTALL)
    if ref_title_match:
        title = ref_title_match.group(1).strip()
        if title:
            reaction_data["reference"] = {"title": title}
    
    # Extract individual yields for each product (using PRO(i):YIELD) and assign them to the corresponding product.
    yield_matches = re.finditer(r'\$DTYPE RXN:VAR\(1\):PRO\((\d+)\):YIELD\s+\$DATUM (\d+)', block)
    yield_dict = { int(m.group(1)) - 1 : int(m.group(2)) for m in yield_matches }
    for (idx, product) in enumerate(products):
        if idx in yield_dict:
             product["yield"] = yield_dict[idx]
    
    return reaction_data

def main():
    input_file = "Valine/valinerdf.txt"
    output_file = "Valine/valine_reactions.json"
    
    reaction_data = extract_reaction_data(input_file)
    
    # Write the data to a JSON file
    with open(output_file, 'w') as file:
        json.dump(reaction_data, file, indent=2)
    
    print(f"Extracted {len(reaction_data)} reactions and saved to {output_file}")

if __name__ == "__main__":
    main() 