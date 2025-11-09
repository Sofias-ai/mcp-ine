#!/usr/bin/env python3
"""
Example: Economic Dashboard
Get the latest economic indicators from INE
"""

from mcp_ine.tools import Get_Latest_Data

def main():
    print("=" * 50)
    print("SPANISH ECONOMIC DASHBOARD")
    print("=" * 50)
    print()
    
    # Consumer Price Index
    print("📊 Consumer Price Index (IPC)")
    try:
        cpi = Get_Latest_Data("IPC")
        print(f"   {cpi}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Industrial Production
    print("🏭 Industrial Production (IPI)")
    try:
        ipi = Get_Latest_Data("IPI")
        print(f"   {ipi}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Housing Prices
    print("🏠 Housing Price Index (IPV)")
    try:
        ipv = Get_Latest_Data("IPV")
        print(f"   {ipv}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Employment
    print("👥 Labor Force Survey (EPA)")
    try:
        epa = Get_Latest_Data("EPA")
        print(f"   {epa}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    print("=" * 50)

if __name__ == "__main__":
    main()
