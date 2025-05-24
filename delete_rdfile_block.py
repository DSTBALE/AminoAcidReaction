#!/usr/bin/env python3

def delete_rdfile_block(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize variables to track the blocks
    start_marker = "M  V30 BEGIN CTAB"
    end_marker = "M  END"
    pattern_to_delete1 = "0  0  0     0  0            999 V3000"
    pattern_to_delete2 = "Copyright (C) 2024 ACS"
    reference_start = "$DTYPE RXN:VAR(1):REFERENCE(1):TITLE"
    exp_proc_start = "$DTYPE RXN:VAR(1):EXP_PROC"
    notes_start = "$DTYPE RXN:VAR(1):NOTES"
    reference_end = "$RFMT"
    rxn_marker = "$RXN"
    mol_marker = "$MOL"
    
    in_block = False
    in_reference_block = False
    in_exp_proc_block = False
    in_notes_block = False
    in_rxn_block = False
    new_lines = []
    
    # Process each line
    for line in lines:
        line = line.rstrip('\n')
        
        # Check if we're at the start of a RXN block
        if rxn_marker in line and not mol_marker in line:
            in_rxn_block = True
            # Keep the $RXN line
            new_lines.append(line + '\n')
            continue
        
        # Check if we've reached a MOL line
        if mol_marker in line:
            in_rxn_block = False
            # Add a blank line before $MOL
            new_lines.append('\n')
            # Keep the $MOL line
            new_lines.append(line + '\n')
            continue
        
        # Check if we're at the start of the RDFile block
        if start_marker in line:
            in_block = True
            continue
        
        # Check if we're at the end of the RDFile block
        if end_marker in line and in_block:
            in_block = False
            continue
        
        # Check if we're at the start of a reference block
        if reference_start in line:
            in_reference_block = True
            continue
        
        # Check if we're at the start of an EXP_PROC block
        if exp_proc_start in line:
            in_exp_proc_block = True
            continue
        
        # Check if we're at the start of a NOTES block
        if notes_start in line:
            in_notes_block = True
            continue
        
        # Check if we're at the end of a block
        if reference_end in line:
            in_reference_block = False
            in_exp_proc_block = False
            in_notes_block = False
            # Add a blank line before $RFMT
            new_lines.append('\n')
            # Keep the $RFMT line
            new_lines.append(line + '\n')
            continue
        
        # Check if the line matches any pattern to delete
        if pattern_to_delete1 in line or pattern_to_delete2 in line:
            continue
        
        # If we're not in any block and the line doesn't match the patterns, keep the line
        if not in_block and not in_reference_block and not in_exp_proc_block and not in_notes_block and not in_rxn_block:
            new_lines.append(line + '\n')
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)
    
    print(f"All specified content has been removed from {file_path}")

if __name__ == "__main__":
    file_path = "Valine/valinerdf.txt"
    delete_rdfile_block(file_path) 