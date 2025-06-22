#!/usr/bin/env python3
"""
Script to split scenes.json into individual scene files.

This script reads the consolidated scenes.json file and creates individual
JSON files for each scene in a scenes/ directory.
"""

import json
import os
from pathlib import Path


def split_scenes_json():
    """
    Split the consolidated scenes.json into individual scene files.
    """
    # Define paths
    current_dir = Path(__file__).parent
    benchmark_dir = current_dir / "libero" / "libero" / "benchmark"
    scenes_json_path = benchmark_dir / "scenes.json"
    scenes_dir = benchmark_dir / "scenes"
    
    # Create scenes directory if it doesn't exist
    scenes_dir.mkdir(exist_ok=True)
    
    # Load the consolidated scenes data
    try:
        with open(scenes_json_path, 'r') as f:
            scenes_data = json.load(f)
        print(f"✓ Loaded scenes data from {scenes_json_path}")
    except FileNotFoundError:
        print(f"✗ Could not find scenes.json at {scenes_json_path}")
        return False
    
    # Split into individual scene files
    scenes = scenes_data.get("scenes", [])
    if not scenes:
        print("✗ No scenes found in the JSON data")
        return False
    
    print(f"Splitting {len(scenes)} scenes into individual files...")
    
    for scene_data in scenes:
        scene_name = scene_data.get("name", "UnknownScene")
        scene_file_path = scenes_dir / f"{scene_name}.json"
        
        # Write individual scene file
        try:
            with open(scene_file_path, 'w') as f:
                json.dump(scene_data, f, indent=4)
            print(f"✓ Created {scene_file_path}")
        except Exception as e:
            print(f"✗ Error creating {scene_file_path}: {e}")
            return False
    
    print(f"\n✓ Successfully split {len(scenes)} scenes into individual files")
    print(f"✓ Scene files created in: {scenes_dir}")
    
    # List created files
    print("\nCreated files:")
    for scene_file in sorted(scenes_dir.glob("*.json")):
        print(f"  - {scene_file.name}")
    
    return True


def main():
    """Main function to execute the scene splitting."""
    print("Splitting scenes.json into individual scene files...")
    print("=" * 60)
    
    success = split_scenes_json()
    
    print("=" * 60)
    if success:
        print("✓ Scene splitting completed successfully!")
        print("\nNext steps:")
        print("1. Update mu_creation_dynamic.py to read from scenes/ directory")
        print("2. Test the new scene loading mechanism")
    else:
        print("✗ Scene splitting failed!")
    
    return success


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
