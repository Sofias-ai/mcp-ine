# Examples for mcp-ine

This directory contains practical examples for using the MCP INE server.

## Example 1: Basic Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ine": {
      "command": "mcp-ine"
    }
  }
}
```

Then ask Claude:
- "¿Cuál es la inflación actual en España?"
- "Show me unemployment trends"
- "Get housing price data"

## Example 2: Python Script - Economic Dashboard

```python
from mcp_ine.tools import Get_Latest_Data

# Get key economic indicators
print("=== Economic Dashboard ===\n")

# Consumer Price Index
cpi = Get_Latest_Data("IPC")
print(f"CPI (latest): {cpi}")

# Industrial Production
ipi = Get_Latest_Data("IPI")
print(f"Industrial Production: {ipi}")

# Housing Prices
ipv = Get_Latest_Data("IPV")
print(f"Housing Prices: {ipv}")

# Employment
epa = Get_Latest_Data("EPA")
print(f"Employment: {epa}")
```

## Example 3: Time Series Analysis

```python
from mcp_ine.tools import Get_Table_Data
import json

# Get 2 years of CPI data
data = Get_Table_Data(
    table_id=50902,      # National CPI
    last_periods=24,     # Last 24 months
    period_type="M"      # Monthly
)

# Print first series
if data:
    series = data[0]
    print(f"\n=== {series['Nombre']} ===")
    for point in series['Data'][:12]:
        print(f"{point['Fecha']}: {point['Valor']}")
```

## Example 4: Regional Comparison

```python
from mcp_ine.tools import Get_Table_Variables, Get_Variable_Values

# Get variables for CPI table
variables = Get_Table_Variables(table_id=50902)
print("Available variables:")
for var in variables[:5]:
    print(f"- {var['Nombre']} (ID: {var['Id']})")

# Get regions
regions = Get_Variable_Values(variable_id=3, table_id=50902)
print("\nAvailable regions:")
for region in regions[:10]:
    print(f"- {region['Nombre']}")
```

## Example 5: Search and Discovery

```python
from mcp_ine.tools import Search_Data, List_Operations

# Search for housing data
print("=== Searching for housing data ===")
results = Search_Data(query="vivienda", max_results=5)
print(json.dumps(results, indent=2, ensure_ascii=False))

# List price-related operations
print("\n=== Price-related operations ===")
operations = List_Operations(filter_text="precio")
for op in operations[:5]:
    print(f"- {op['Nombre']} ({op['Codigo']})")
```

## Running the Examples

1. Install the package:
```bash
pip install mcp-ine
```

2. Run any example:
```bash
python example_economic_dashboard.py
```

## Need Help?

- Documentation: https://github.com/Sofias-ai/mcp-ine
- Issues: https://github.com/Sofias-ai/mcp-ine/issues
- PyPI: https://pypi.org/project/mcp-ine/
