def extract_single_stage_reactions(input_file, output_file):
    """
    Extract reactions that only have one stage (only "1.1" and no "1.2", "1.3", etc.)
    from the input file and write them to the output file.
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output text file
    """
    
    single_stage_reactions = []
    current_reaction = []
    current_reaction_stages = set()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                # If we have a current reaction and it only has stage 1.1, save it
                if current_reaction and current_reaction_stages == {'1.1'}:
                    single_stage_reactions.extend(current_reaction)
                    single_stage_reactions.append('')  # Add empty line for separation
                
                # Reset for next reaction
                current_reaction = []
                current_reaction_stages = set()
                continue
            
            # Add line to current reaction
            current_reaction.append(line)
            
            # Check if this line contains a stage number
            if '|' in line and not line.startswith('CAS Reaction Number:'):
                # Check if it's a continuation line (starts with "|")
                if line.startswith('|'):
                    # This is a continuation line, don't treat as new stage
                    continue
                else:
                    # Extract stage number (e.g., "1.1", "1.2", etc.)
                    stage_part = line.split('|')[0]
                    current_reaction_stages.add(stage_part)
        
        # Handle the last reaction if file doesn't end with empty line
        if current_reaction and current_reaction_stages == {'1.1'}:
            single_stage_reactions.extend(current_reaction)
        
        # Write single-stage reactions to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in single_stage_reactions:
                f.write(line + '\n')
        
        print(f"Successfully extracted single-stage reactions!")
        print(f"Total single-stage reactions found: {len([r for r in single_stage_reactions if r.startswith('CAS Reaction Number:')])}")
        print(f"Results saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    """Main function to run the extraction"""
    input_file = "Asparagine/combine_cleaned.txt"
    output_file = "Asparagine/combine_single_stage_reactions.txt"
    
    print("Starting extraction of single-stage reactions...")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("-" * 50)
    
    extract_single_stage_reactions(input_file, output_file)


if __name__ == "__main__":
    main() 