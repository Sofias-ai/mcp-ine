#!/usr/bin/env python3
"""
Example: Time Series Analysis
Analyze CPI trends over the last 2 years
"""

from mcp_ine.tools import Get_Table_Data
import json

def main():
    print("=" * 50)
    print("CPI TIME SERIES ANALYSIS")
    print("=" * 50)
    print()
    
    print("Fetching last 24 months of CPI data...")
    
    try:
        # Get 2 years of monthly CPI data
        data = Get_Table_Data(
            table_id=50902,      # National CPI table
            last_periods=24,     # Last 24 months
            period_type="M"      # Monthly data
        )
        
        if data and len(data) > 0:
            # Get the general CPI series
            series = data[0]
            print(f"\n📈 Series: {series.get('Nombre', 'Unknown')}")
            print(f"   Unit: {series.get('FK_Unidad', 'N/A')}")
            print(f"   Scale: {series.get('FK_Escala', 'N/A')}")
            print()
            
            # Print recent data points
            print("Recent values:")
            print("-" * 40)
            data_points = series.get('Data', [])[:12]
            for point in data_points:
                fecha = point.get('Fecha', 'N/A')
                valor = point.get('Valor', 'N/A')
                print(f"{fecha}: {valor}")
            
            # Calculate trend
            if len(data_points) >= 2:
                first_val = float(data_points[-1].get('Valor', 0))
                last_val = float(data_points[0].get('Valor', 0))
                change = last_val - first_val
                pct_change = (change / first_val) * 100 if first_val else 0
                
                print()
                print(f"📊 12-month change: {change:.2f} ({pct_change:.2f}%)")
        else:
            print("No data available")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
