#!/usr/bin/env python3
"""
Dead Code Ghostbuster - Exorcises unused code from your haunted codebase.
Because ghosts don't pay rent, and neither should dead code.
"""

import ast
import os
import sys
from collections import defaultdict


def find_python_files(directory):
    """Find Python files like a ghost hunter with a proton pack."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)


def extract_imports_and_defs(filepath):
    """Extract imports and function definitions - the usual ghost suspects."""
    with open(filepath, 'r') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return set(), set()
    
    imports = set()
    definitions = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions.add(node.name)
    
    return imports, definitions


def find_unused_imports(all_imports, all_defs):
    """Find imports that are just haunting your imports section."""
    used_imports = set()
    for file_imports, file_defs in zip(all_imports, all_defs):
        used_imports.update(file_imports.intersection(file_defs))
    
    all_imports_flat = set().union(*all_imports)
    return all_imports_flat - used_imports


def main():
    """Main exorcism ritual - say the magic words: 'python ghostbuster.py'."""
    if len(sys.argv) != 2:
        print("Usage: python dead_code_ghostbuster.py <directory>")
        print("Example: python dead_code_ghostbuster.py ./src")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    print(f"\n🔦 Ghostbusting in {directory}...")
    
    all_imports = []
    all_defs = []
    
    for filepath in find_python_files(directory):
        imports, defs = extract_imports_and_defs(filepath)
        all_imports.append(imports)
        all_defs.append(defs)
    
    unused_imports = find_unused_imports(all_imports, all_defs)
    
    if unused_imports:
        print("\n👻 Potential ghost imports (unused):")
        for imp in sorted(unused_imports):
            print(f"  - {imp}")
        print(f"\nTotal ghosts found: {len(unused_imports)}")
        print("\n💀 Remember: Not all ghosts are harmful, but they're all creepy.")
        print("   Review before deleting - some imports might be used indirectly!")
    else:
        print("\n✨ No ghost imports found! Your codebase is spiritually clean!")


if __name__ == "__main__":
    main()
