#!/usr/bin/env python3
"""
Script to extract scene definitions from mu_creation.py and convert them to JSON format.
The extracted JSON will follow the structure defined in sample_scene.json.
"""

import ast
import json
import re
import math
from typing import Dict, List, Any, Tuple

class SceneExtractor:
    def __init__(self, source_file: str):
        self.source_file = source_file
        self.scenes = []
        self.scene_mapping = {}  # Maps original class name to new scene name
        
    def extract_scenes(self):
        """Extract all scene definitions from the source file."""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the Python file
        tree = ast.parse(content)
        
        scene_counter = 1
        
        # Find all class definitions with @register_mu decorator
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class has @register_mu decorator
                for decorator in node.decorator_list:
                    if (isinstance(decorator, ast.Call) and 
                        isinstance(decorator.func, ast.Name) and 
                        decorator.func.id == 'register_mu'):
                        
                        # Extract scene type
                        scene_type = None
                        for keyword in decorator.keywords:
                            if keyword.arg == 'scene_type':
                                scene_type = keyword.value.s
                        
                        if scene_type:
                            scene_data = self.extract_scene_data(node, content)
                            if scene_data:
                                scene_name = f"Scene{scene_counter}"
                                self.scene_mapping[node.name] = scene_name
                                scene_data['name'] = scene_name
                                scene_data['original_class'] = node.name
                                scene_data['scene_type'] = scene_type
                                self.scenes.append(scene_data)
                                scene_counter += 1
        
        return self.scenes, self.scene_mapping
    
    def extract_scene_data(self, class_node: ast.ClassDef, content: str) -> Dict[str, Any]:
        """Extract scene data from a class definition."""
        scene_data = {
            'fixture_num_info': {},
            'object_num_info': {},
            'regions': [],
            'init_states': []
        }
        
        # Extract __init__ method for fixture_num_info and object_num_info
        init_method = None
        define_regions_method = None
        init_states_property = None
        
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                if node.name == '__init__':
                    init_method = node
                elif node.name == 'define_regions':
                    define_regions_method = node
                # Check for init_states property
                if hasattr(node, 'decorator_list') and len(node.decorator_list) > 0:
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == 'property':
                            if node.name == 'init_states':
                                init_states_property = node
        
        # Extract fixture_num_info and object_num_info from __init__
        if init_method:
            self.extract_init_data(init_method, scene_data)
        
        # Extract regions from define_regions method
        if define_regions_method:
            self.extract_regions_data(define_regions_method, content, scene_data)
        
        # Extract init_states from property
        if init_states_property:
            self.extract_init_states_data(init_states_property, content, scene_data)
        
        return scene_data
    
    def extract_init_data(self, init_method: ast.FunctionDef, scene_data: Dict[str, Any]):
        """Extract fixture_num_info and object_num_info from __init__ method."""
        for node in ast.walk(init_method):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == 'fixture_num_info' and isinstance(node.value, ast.Dict):
                            scene_data['fixture_num_info'] = self.extract_dict_from_ast(node.value)
                        elif target.id == 'object_num_info' and isinstance(node.value, ast.Dict):
                            scene_data['object_num_info'] = self.extract_dict_from_ast(node.value)
    
    def extract_dict_from_ast(self, dict_node: ast.Dict) -> Dict[str, Any]:
        """Extract dictionary from AST Dict node."""
        result = {}
        for key, value in zip(dict_node.keys, dict_node.values):
            if isinstance(key, ast.Str):
                key_str = key.s
            elif isinstance(key, ast.Constant):
                key_str = key.value
            else:
                continue
                
            if isinstance(value, ast.Num):            result[key_str] = value.n
            elif isinstance(value, ast.Constant):
                result[key_str] = value.value
        return result
    
    def extract_regions_data(self, define_regions_method: ast.FunctionDef, content: str, scene_data: Dict[str, Any]):
        """Extract regions data by parsing the method source."""
        # Get the source lines for this method
        start_line = define_regions_method.lineno
        end_line = define_regions_method.end_lineno if hasattr(define_regions_method, 'end_lineno') else start_line + 50
        
        lines = content.split('\n')
        method_source = '\n'.join(lines[start_line-1:end_line])
        
        # Find all get_region_dict calls with balanced parentheses
        region_calls = self.extract_balanced_function_calls(method_source, 'self.get_region_dict')
        
        for call in region_calls:
            region_data = self.parse_region_call(call)
            if region_data:
                scene_data['regions'].append(region_data)
    
    def extract_balanced_function_calls(self, source: str, function_name: str) -> List[str]:
        """Extract function calls with balanced parentheses."""
        calls = []
        pattern = re.escape(function_name) + r'\s*\('
        
        for match in re.finditer(pattern, source):
            start_pos = match.end() - 1  # Position of opening parenthesis
            paren_count = 0
            end_pos = start_pos
            
            for i, char in enumerate(source[start_pos:], start_pos):
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        end_pos = i
                        break
            
            if paren_count == 0:  # Found balanced parentheses
                call_content = source[start_pos + 1:end_pos]  # Extract content between parentheses
                calls.append(call_content)
        
        return calls
    
    def parse_region_call(self, call_args: str) -> Dict[str, Any]:
        """Parse a get_region_dict call to extract region data."""
        try:
            region_data = {
                'region_centroid_xy': [0.0, 0.0],
                'region_name': '',
                'region_half_len': 0.025,
                'yaw_rotation': [0.0, 0.0]
            }
            
            # Extract region_centroid_xy
            xy_match = re.search(r'region_centroid_xy=\[(.*?)\]', call_args)
            if xy_match:
                coords = [float(x.strip()) for x in xy_match.group(1).split(',')]
                region_data['region_centroid_xy'] = coords
            
            # Extract region_name
            name_match = re.search(r'region_name="([^"]*)"', call_args)
            if name_match:
                region_data['region_name'] = name_match.group(1)
            
            # Extract region_half_len
            len_match = re.search(r'region_half_len=([\d.]+)', call_args)
            if len_match:
                region_data['region_half_len'] = float(len_match.group(1))
            
            # Extract yaw_rotation - this can span multiple lines
            yaw_match = re.search(r'yaw_rotation=\((.*?)\)', call_args, re.DOTALL)
            if yaw_match:
                yaw_content = yaw_match.group(1).strip()
                # Remove any newlines and extra spaces
                yaw_content = re.sub(r'\s+', ' ', yaw_content).strip()
                
                # Handle different formats
                if 'np.pi' in yaw_content:
                    # Split by comma and process each part
                    parts = [part.strip() for part in yaw_content.split(',')]
                    yaw_values = []
                    for part in parts:
                        if part == 'np.pi':
                            yaw_values.append(1.0)
                        elif part == '0':
                            yaw_values.append(0.0)
                        elif 'np.pi' in part:
                            # Handle expressions like -np.pi/2
                            if part.startswith('-'):
                                if '/2' in part:
                                    yaw_values.append(-0.5)
                                elif '/4' in part:
                                    yaw_values.append(-0.25)
                                else:
                                    yaw_values.append(-1.0)
                            else:
                                if '/2' in part:
                                    yaw_values.append(0.5)
                                elif '/4' in part:
                                    yaw_values.append(0.25)
                                else:
                                    yaw_values.append(1.0)
                        else:
                            try:
                                yaw_values.append(float(part))
                            except:
                                yaw_values.append(0.0)
                    
                    if len(yaw_values) >= 2:
                        region_data['yaw_rotation'] = yaw_values[:2]
                    elif len(yaw_values) == 1:
                        region_data['yaw_rotation'] = [yaw_values[0], 0.0]
                        
                elif yaw_content in ['0, 0', '(0, 0)']:
                    region_data['yaw_rotation'] = [0.0, 0.0]
                else:
                    # Try to parse as numbers
                    try:
                        vals = [x.strip() for x in yaw_content.split(',')]
                        yaw_values = [float(val) for val in vals if val]
                        region_data['yaw_rotation'] = yaw_values[:2] if len(yaw_values) >= 2 else [0.0, 0.0]
                    except:
                        region_data['yaw_rotation'] = [0.0, 0.0]
            
            return region_data
        except Exception as e:
            print(f"Error parsing region call: {e}")
            return None
    
    def extract_init_states_data(self, init_states_property: ast.FunctionDef, content: str, scene_data: Dict[str, Any]):
        """Extract init_states data from the property method."""
        # Get the source lines for this method
        start_line = init_states_property.lineno
        end_line = init_states_property.end_lineno if hasattr(init_states_property, 'end_lineno') else start_line + 50
        
        lines = content.split('\n')
        method_source = '\n'.join(lines[start_line-1:end_line])
        
        # Find states list - handle both "states = [" and direct "return [" patterns
        states_match = re.search(r'states = \[(.*?)\]', method_source, re.DOTALL)
        if not states_match:
            # Try to find return statement with list
            states_match = re.search(r'return \[(.*?)\]', method_source, re.DOTALL)
        
        if states_match:
            states_content = states_match.group(1)
            
            # Use regex to find all tuple patterns
            tuple_pattern = r'\((.*?)\)'
            tuples = re.findall(tuple_pattern, states_content, re.DOTALL)
            
            for tuple_content in tuples:
                self.parse_single_state_tuple(tuple_content, scene_data)
    
    def parse_single_state_tuple(self, tuple_str: str, scene_data: Dict[str, Any]):
        """Parse a single state tuple string."""
        try:
            # Clean up the tuple content and split by commas
            tuple_str = tuple_str.strip()
            
            # Split by comma, being careful about quoted strings
            parts = []
            current_part = ""
            in_quotes = False
            quote_char = None
            
            for char in tuple_str:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                elif char == ',' and not in_quotes:
                    parts.append(current_part.strip().strip('"').strip("'"))
                    current_part = ""
                    continue
                current_part += char
            
            # Add the last part
            if current_part:
                parts.append(current_part.strip().strip('"').strip("'"))
            
            # Clean up parts and filter out empty ones
            cleaned_parts = [part.strip() for part in parts if part.strip()]
            
            if len(cleaned_parts) >= 2:
                scene_data['init_states'].append(cleaned_parts)
                
        except Exception as e:
            print(f"Error parsing state tuple '{tuple_str}': {e}")
    
    def replace_table_names(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """Replace specific table names with {scene_table} placeholder."""
        table_mappings = {
            'kitchen_table': '{scene_table}',
            'living_room_table': '{scene_table}',
            'study_table': '{scene_table}',
            'main_table': '{scene_table}'
        }
        
        # Replace in fixture_num_info
        new_fixture_info = {}
        for key, value in scene_data['fixture_num_info'].items():
            new_key = table_mappings.get(key, key)
            new_fixture_info[new_key] = value
        scene_data['fixture_num_info'] = new_fixture_info
        
        # Replace in init_states
        new_init_states = []
        for state in scene_data['init_states']:
            new_state = []
            for part in state:
                new_part = part
                for old_table, new_table in table_mappings.items():
                    new_part = new_part.replace(old_table, new_table)
                new_state.append(new_part)
            new_init_states.append(new_state)
        scene_data['init_states'] = new_init_states
        
        return scene_data
    
    def generate_json(self, output_file: str):
        """Generate the final JSON file."""
        scenes, mapping = self.extract_scenes()
        
        json_data = {
            'scenes': []
        }
        
        for scene in scenes:
            # Replace table names with placeholders
            scene = self.replace_table_names(scene)
            
            # Remove extra fields for JSON output
            json_scene = {
                'name': scene['name'],
                'fixture_num_info': scene['fixture_num_info'],
                'object_num_info': scene['object_num_info'],
                'regions': scene['regions'],
                'init_states': scene['init_states']
            }
            
            json_data['scenes'].append(json_scene)
        
        # Write JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        
        # Write mapping file
        mapping_file = output_file.replace('.json', '_mapping.json')
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=4, ensure_ascii=False)
        
        print(f"Extracted {len(scenes)} scenes to {output_file}")
        print(f"Scene mapping saved to {mapping_file}")
        
        return json_data, mapping

def main():
    """Main function to run the extraction."""
    source_file = "../libero/libero/benchmark/mu_creation.py"
    output_file = "../scenes.json"
    
    extractor = SceneExtractor(source_file)
    json_data, mapping = extractor.generate_json(output_file)
    
    print("\nScene mapping:")
    for original, new in mapping.items():
        print(f"{original} -> {new}")

if __name__ == "__main__":
    main()
