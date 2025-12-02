import pandas as pd
import numpy as np

# This will use the MCP tool to query each team member separately
# For now, let me create a script that processes the data we already have
# and combines it with the tracker merchant assignments

print("Team Commission Rate Analysis")
print("="*60)
print("This script will query each team member's GMV and commission data")
print("using merchant IDs from the Penang tracker file")
print()
print("Note: Due to query size limitations, we'll process this in Python")
print("by reading the tracker and creating efficient queries")

