#!/usr/bin/env python3
"""
Script to extend tasks from the tasks directory to other scene types.
This script converts tasks to Kitchen, Study, and Tabletop Manipulation scenes
and saves them to the tasks_extended directory.
"""

import re
from pathlib import Path

# Constants for table heights (from mu_creation.py)
KITCHEN_TABLE_HEIGHT = 0.875
LIVING_ROOM_TABLE_HEIGHT = 0.41
STUDY_TABLE_HEIGHT = 0.67
TABLE_HEIGHT = 0.895

def get_scene_mappings():
    """Define the scene type mappings"""
    return {
        'kitchen': {
            'suffix': '_kitchen',
            'table_height': KITCHEN_TABLE_HEIGHT,
            'import_statement': 'from libero.libero.benchmark import *',
        },
        'study': {
            'suffix': '_study', 
            'table_height': STUDY_TABLE_HEIGHT,
            'import_statement': 'from libero.libero.benchmark import *',
        },
        'tabletop_manipulation': {
            'suffix': '_tabletop_manipulation',
            'table_height': TABLE_HEIGHT,
            'import_statement': 'from libero.libero.benchmark import *',
        },
        'living_room': {
            'suffix': '_living_room',
            'table_height': LIVING_ROOM_TABLE_HEIGHT,
            'import_statement': 'from libero.libero.benchmark import *',
        }
    }

def extract_scene_info(filename):
    """Extract scene type and scene number from filename"""
    # Pattern to match scene files like LIVING_ROOM_SCENE2_task.py or KITCHEN_SCENE1_task.py
    pattern = r'^([A-Z_]+_SCENE\d+)_(.+)\.py$'
    match = re.match(pattern, filename)
    
    if not match:
        return None, None, None
        
    scene_prefix = match.group(1)  # e.g., LIVING_ROOM_SCENE2
    task_description = match.group(2)  # e.g., push_the_milk_until_it_contacts_the_orange_juice
    
    # Determine original scene type
    if scene_prefix.startswith('KITCHEN_'):
        original_type = 'kitchen'
    elif scene_prefix.startswith('LIVING_ROOM_'):
        original_type = 'living_room'
    elif scene_prefix.startswith('STUDY_'):
        original_type = 'study'
    elif scene_prefix.startswith('TABLETOP_'):
        original_type = 'tabletop'
    else:
        return None, None, None
        
    return scene_prefix, task_description, original_type

def get_original_table_height(original_type):
    """Get the table height for the original scene type"""
    height_map = {
        'kitchen': KITCHEN_TABLE_HEIGHT,
        'living_room': LIVING_ROOM_TABLE_HEIGHT,
        'study': STUDY_TABLE_HEIGHT,
        'tabletop': TABLE_HEIGHT
    }
    return height_map.get(original_type, 0.5)

def convert_scene_name(scene_name, target_scene_type):
    """Convert scene name to the target scene type format"""
    if target_scene_type == 'tabletop_manipulation':
        return scene_name + '_tabletop_manipulation'
    elif target_scene_type == 'kitchen':
        return scene_name + '_kitchen'
    elif target_scene_type == 'study':
        return scene_name + '_study'
    elif target_scene_type == 'living_room':
        return scene_name + '_living_room'
    return scene_name

def update_position_within_coordinates(line, original_type, target_type):
    """Update coordinates for table height differences in PositionWithin, PosiGreaterThan, and InAir constraints"""
    # Check if this line contains any height-related constraints
    if not any(constraint in line for constraint in ['PositionWithin', 'PosiGreaterThan', 'InAir']):
        return line
        
    # Get table height constants for different scene types
    def get_table_height_constant(scene_type):
        if scene_type == 'kitchen':
            return 'KITCHEN_TABLE_HEIGHT'
        elif scene_type == 'living_room':
            return 'LIVING_ROOM_TABLE_HEIGHT'
        elif scene_type == 'study':
            return 'STUDY_TABLE_HEIGHT'
        elif scene_type == 'tabletop' or scene_type == 'tabletop_manipulation':
            return 'TABLE_HEIGHT'
        return 'LIVING_ROOM_TABLE_HEIGHT'  # default fallback
    
    original_height_const = get_table_height_constant(original_type)
    target_height_const = get_table_height_constant(target_type)
    
    # Look for existing height adjustments and replace them
    # Pattern for existing height calculations like "0.5 - LIVING_ROOM_TABLE_HEIGHT + TABLE_HEIGHT"
    height_calc_pattern = r'(\d+\.?\d*)\s*-\s*[A-Z_]+_TABLE_HEIGHT\s*\+\s*[A-Z_]+_TABLE_HEIGHT'
    
    if re.search(height_calc_pattern, line):
        # Replace existing height calculation with correct original and target heights
        replacement = rf'\1 - {original_height_const} + {target_height_const}'
        line = re.sub(height_calc_pattern, replacement, line)
    else:        # Look for simple z coordinates and add height adjustment if needed
        # We need to preserve the original indentation and formatting
        # First, capture the leading whitespace
        leading_whitespace_match = re.match(r'^(\s*)', line)
        leading_whitespace = leading_whitespace_match.group(1) if leading_whitespace_match else ''
        
        # Handle different constraint types
        if 'PositionWithin' in line:
            # Pattern to match PositionWithin tuples more carefully
            pos_pattern = r'(\("PositionWithin",\s*"[^"]+",\s*[^,]+,\s*[^,]+,\s*)([^,]+)(,.*?\))'
            match = re.search(pos_pattern, line)
            
            if match and original_type != target_type:
                prefix = match.group(1)
                z_coord = match.group(2).strip()
                suffix = match.group(3)
                
                # Add height adjustment calculation using correct original height
                new_z_coord = f"{z_coord} - {original_height_const} + {target_height_const}"
                line = prefix + new_z_coord + suffix
                
                # Ensure the line ends with a comma if it's part of a list/tuple
                if not line.rstrip().endswith(','):
                    line = line.rstrip() + ','
                
                # Preserve original indentation
                if not line.startswith(leading_whitespace):
                    line = leading_whitespace + line.lstrip()
        
        # Handle PosiGreaterThan constraints - pattern: ("PosiGreaterThan", "object", "z", value)
        elif 'PosiGreaterThan' in line and '"z"' in line:
            posi_pattern = r'(\("PosiGreaterThan",\s*"[^"]+",\s*"z",\s*)([^,\)]+)(\s*\))'
            match = re.search(posi_pattern, line)
            
            if match and original_type != target_type:
                prefix = match.group(1)
                z_value = match.group(2).strip()
                suffix = match.group(3)
                
                # Add height adjustment calculation
                new_z_value = f"{z_value} - {original_height_const} + {target_height_const}"
                line = prefix + new_z_value + suffix
                
                # Ensure proper formatting
                if not line.rstrip().endswith(','):
                    line = line.rstrip() + ','
                
                # Preserve original indentation
                if not line.startswith(leading_whitespace):
                    line = leading_whitespace + line.lstrip()
        
        # Handle InAir constraints - pattern: ("InAir", "object", height_value)
        elif 'InAir' in line:
            inair_pattern = r'(\("InAir",\s*"[^"]+",\s*)([^,\)]+)(\s*\))'
            match = re.search(inair_pattern, line)
            
            if match and original_type != target_type:
                prefix = match.group(1)
                height_value = match.group(2).strip()
                suffix = match.group(3)
                
                # Add height adjustment calculation
                new_height_value = f"{height_value} - {original_height_const} + {target_height_const}"
                line = prefix + new_height_value + suffix
                
                # Ensure proper formatting
                if not line.rstrip().endswith(','):
                    line = line.rstrip() + ','
                
                # Preserve original indentation
                if not line.startswith(leading_whitespace):
                    line = leading_whitespace + line.lstrip()
            
    return line

def process_task_file(input_file, output_file, target_scene_type, original_type):
    """Process a single task file and convert it to the target scene type"""
    mappings = get_scene_mappings()
    target_mapping = mappings[target_scene_type]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # Update the filepath comment
        if line.startswith('# filepath:'):
            processed_lines.append(f'# filepath: {output_file}')
            
        # Update imports - replace mu_creation import with benchmark import
        elif 'from libero.libero.benchmark.mu_creation import' in line:
            processed_lines.append(target_mapping['import_statement'])
            
        # Update scene_name in main function
        elif 'scene_name =' in line and '"' in line:
            # Extract the scene name and convert it
            pattern = r'scene_name\s*=\s*"([^"]+)"'
            match = re.search(pattern, line)
            if match:
                original_scene_name = match.group(1)
                new_scene_name = convert_scene_name(original_scene_name, target_scene_type)
                line = line.replace(f'"{original_scene_name}"', f'"{new_scene_name}"')
            processed_lines.append(line)
              # Update PositionWithin, PosiGreaterThan, and InAir coordinates for table height differences
        elif any(constraint in line for constraint in ['PositionWithin', 'PosiGreaterThan', 'InAir']):
            line = update_position_within_coordinates(line, original_type, target_scene_type)
            processed_lines.append(line)
            
        else:
            processed_lines.append(line)
    
    # Write the processed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines))

def main():
    """Main function to process all task files"""
    # Set up directories
    tasks_dir = Path('c:/Users/adlsdztony/code/VLA/LIBERO/tasks')
    tasks_extended_dir = Path('c:/Users/adlsdztony/code/VLA/LIBERO/tasks_extended')
    
    # Create tasks_extended directory if it doesn't exist
    tasks_extended_dir.mkdir(exist_ok=True)
    
    # Get all task files
    task_files = [f for f in tasks_dir.glob('*.py') if f.is_file()]
    
    print(f"Found {len(task_files)} task files to process...")
    
    scene_mappings = get_scene_mappings()
    processed_count = 0
    skipped_count = 0
    
    for task_file in task_files:
        filename = task_file.name
        print(f"Processing: {filename}")
        
        # Extract scene information
        scene_prefix, task_description, original_type = extract_scene_info(filename)
        
        if not scene_prefix:
            print(f"  Skipped: Could not parse scene info from {filename}")
            skipped_count += 1
            continue
            
        # Create extended versions for each target scene type
        for target_type, mapping in scene_mappings.items():
            # Skip if converting to the same type
            if target_type == original_type:
                continue
                  # Generate output filename
            if target_type == 'tabletop_manipulation':
                suffix = '_TABLETOP_MANIPULATION'
            elif target_type == 'kitchen':
                suffix = '_KITCHEN'
            elif target_type == 'study':
                suffix = '_STUDY'
            elif target_type == 'living_room':
                suffix = '_LIVING_ROOM'
            else:
                suffix = f'_{target_type.upper()}'
                
            output_filename = f"{scene_prefix}{suffix}_{task_description}.py"
            output_file = tasks_extended_dir / output_filename
            
            # Process the file
            try:
                process_task_file(task_file, output_file, target_type, original_type)
                print(f"  Created: {output_filename}")
                processed_count += 1
            except Exception as e:
                print(f"  Error processing {filename} -> {target_type}: {e}")
                continue
    
    print("\nProcessing complete!")
    print(f"Processed: {processed_count} extended task files")
    print(f"Skipped: {skipped_count} files")
    print(f"Results saved to: {tasks_extended_dir}")

if __name__ == "__main__":
    main()
