#!/usr/bin/env python3
"""
Script to generate Kodi repository files (addons.xml and addons.xml.md5)
and package addons into zip files.

Usage:
    python3 generate_repo.py [output_dir]

Arguments:
    output_dir - Optional output directory (default: repo)
"""

import os
import sys
import shutil
import hashlib
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def get_addon_dirs():
    """Get all addon directories (starting with 'plugin.', 'service.', 'context.', or 'repository.')"""
    base_path = Path(__file__).parent.parent
    addon_dirs = []
    
    for item in base_path.iterdir():
        if item.is_dir() and (
            item.name.startswith('plugin.') or 
            item.name.startswith('service.') or 
            item.name.startswith('context.') or 
            item.name.startswith('repository.')
        ):
            addon_xml = item / 'addon.xml'
            if addon_xml.exists():
                addon_dirs.append(item)
    
    return addon_dirs


def get_addon_info(addon_dir):
    """Extract addon id and version from addon.xml"""
    addon_xml = addon_dir / 'addon.xml'
    tree = ET.parse(addon_xml)
    root = tree.getroot()
    
    addon_id = root.get('id')
    version = root.get('version')
    
    return addon_id, version, tree


def create_zip(addon_dir, addon_id, version, output_dir):
    """Create a zip file for the addon"""
    zip_filename = f"{addon_id}-{version}.zip"
    zip_path = output_dir / zip_filename
    
    print(f"Creating {zip_filename}...")
    
    # Remove old zip if exists
    if zip_path.exists():
        zip_path.unlink()
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(addon_dir):
            # Skip hidden files and directories, and __pycache__
            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                file_path = Path(root) / file
                arcname = Path(addon_id) / file_path.relative_to(addon_dir)
                zipf.write(file_path, arcname)
    
    print(f"Created {zip_filename}")
    return zip_filename


def indent_xml(elem, level=0):
    """Add pretty-printing indentation to XML (for Python < 3.9 compatibility)"""
    indent = "\n" + "    " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            indent_xml(child, level + 1)
        # Update tail for last child
        if len(elem) > 0:
            last_child = elem[-1]
            if not last_child.tail or not last_child.tail.strip():
                last_child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def generate_addons_xml(addon_dirs, output_dir):
    """Generate addons.xml file"""
    print("Generating addons.xml...")
    
    root = ET.Element('addons')
    
    for addon_dir in addon_dirs:
        addon_id, version, tree = get_addon_info(addon_dir)
        addon_element = tree.getroot()
        root.append(addon_element)
    
    # Create tree and write to file
    tree = ET.ElementTree(root)
    indent_xml(root)

    addons_xml_path = output_dir / 'addons.xml'
    tree.write(addons_xml_path, encoding='utf-8', xml_declaration=True)
    
    print(f"Generated addons.xml")
    return addons_xml_path


def generate_md5(file_path):
    """Generate MD5 hash for a file"""
    print(f"Generating MD5 for {file_path.name}...")
    
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        md5_hash.update(f.read())
    
    md5_file = file_path.parent / f"{file_path.name}.md5"
    with open(md5_file, 'w') as f:
        f.write(md5_hash.hexdigest())
    
    print(f"Generated {md5_file.name}")


def main():
    """Main function"""
    base_path = Path(__file__).parent.parent
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        output_arg = sys.argv[1]
        # Validate path - must be relative or within base_path
        # Prevent directory traversal attacks
        if '..' in output_arg or output_arg.startswith('/'):
            print(f"Error: Invalid output directory '{output_arg}'")
            print("Output directory must be a relative path without '..'")
            sys.exit(1)
        repo_dir = base_path / output_arg
    else:
        repo_dir = base_path / 'repo'
    
    print(f"Output directory: {repo_dir}")
    
    # Create repo directory if it doesn't exist
    repo_dir.mkdir(exist_ok=True)
    
    # Get all addon directories
    addon_dirs = get_addon_dirs()
    
    if not addon_dirs:
        print("No addon directories found!")
        return
    
    print(f"Found {len(addon_dirs)} addon(s)")
    
    # Create subdirectories for each addon
    for addon_dir in addon_dirs:
        addon_id, _, _ = get_addon_info(addon_dir)
        addon_output_dir = repo_dir / addon_id
        addon_output_dir.mkdir(exist_ok=True)
    
    # Create zip files for each addon
    for addon_dir in addon_dirs:
        addon_id, version, _ = get_addon_info(addon_dir)
        addon_output_dir = repo_dir / addon_id
        
        # Create ZIP in addon subdirectory
        create_zip(addon_dir, addon_id, version, addon_output_dir)
        
        # Copy icon.png if exists
        icon_path = addon_dir / 'icon.png'
        if icon_path.exists():
            shutil.copy(icon_path, addon_output_dir / 'icon.png')
            print(f"Copied icon.png for {addon_id}")
        
        # Copy fanart.jpg if exists
        fanart_path = addon_dir / 'fanart.jpg'
        if fanart_path.exists():
            shutil.copy(fanart_path, addon_output_dir / 'fanart.jpg')
            print(f"Copied fanart.jpg for {addon_id}")
    
    # Generate addons.xml
    addons_xml_path = generate_addons_xml(addon_dirs, repo_dir)
    
    # Generate MD5 for addons.xml
    generate_md5(addons_xml_path)
    
    print("\nRepository generation complete!")
    print(f"Repository files are in: {repo_dir}")


if __name__ == '__main__':
    main()
