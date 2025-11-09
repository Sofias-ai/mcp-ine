#!/usr/bin/env python3
"""
Example: Search and Discovery
Find relevant datasets using search and filters
"""

from mcp_ine.tools import Search_Data, List_Operations
import json

def main():
    print("=" * 50)
    print("SEARCH AND DISCOVERY")
    print("=" * 50)
    print()
    
    # Search for housing-related data
    print("🔍 Searching for 'vivienda' (housing)...")
    try:
        results = Search_Data(query="vivienda", max_results=5)
        print(f"Found {len(results)} operations/tables:")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("-" * 50)
    print()
    
    # List price-related operations
    print("💰 Price-related operations...")
    try:
        operations = List_Operations(filter_text="precio")
        print(f"Found {len(operations)} operations:")
        for op in operations[:10]:
            print(f"  - {op.get('Nombre', 'N/A')} ({op.get('Codigo', 'N/A')})")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("-" * 50)
    print()
    
    # Search for employment data
    print("👥 Searching for employment data...")
    try:
        results = Search_Data(query="empleo", max_results=3)
        print(f"Found {len(results)} results:")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
