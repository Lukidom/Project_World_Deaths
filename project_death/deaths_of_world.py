import sys
from pathlib import Path
import pandas as pd

# visual check for proper path finding
print("before read csv")

#  Check if the CSV file exists in the expected location
csv_path = Path(__file__).parent / "deaths_of_world.csv"

# Check if the file does not exist
if not csv_path.exists():
	print(f"ERROR: CSV not found at {csv_path}")
	sys.exit(1)
	
def print_file_general(csv_path):
    print(f"CSV file found at: {csv_path}")
    print(f"File size: {csv_path.stat().st_size} bytes")
    print("--------------------------------")
    # read the CSV file with specified encoding and handle bad lines or errors
    try:
        df = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
        # basic check for proper reading
        print("after read csv")
        # print basic info
        print("shape:", df.shape)
        print("columns:", list(df.columns))
        print(df.head())

        print("-----------------------------------")
        # Example aggregation (guard against missing columns) (kind of unnecessary) 
        # Simple for loop to assign columns to to_drop if they exist in df
        to_drop = [c for c in ['Entity', 'Code', 'Year'] if c in df.columns]

        # If statement to check if to_drop is empty then performs drop and sum
        if to_drop:
            # Prints sum of numeric columns 
            print("sum of remaining numeric columns:")
            # Drop specified columns and sum the rest with a check for numeric only
            print(df.drop(columns=to_drop).sum(numeric_only=True))
        else:
            # else is for error handling if no columns to drop
            print("No Entity/Code/Year columns to drop for aggregation")
    except Exception as e:
        print("Failed to read or process CSV:", e)
        raise



def print_file_year_info(csv_path):
    try:
         df = pd.read_csv(csv_path, encoding="lain1", on_bad_lines="skip")
# Trying to figure out how to iterate through the countries then years to find out trends in the last ten years for deaths accross the world. 
