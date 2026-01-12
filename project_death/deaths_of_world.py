import sys
from pathlib import Path
import pandas as pd


def print_file_general(csv_path):
    print(f"CSV file found at: {csv_path}")
    print(f"File size: {csv_path.stat().st_size} bytes")
    print("--------------------------------")
    # read the CSV file with specified encoding and handle bad lines or errors
    # Simple aggregation
    # Try syntaz and statements to catch errors
    try:
        df = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
        # basic check for proper reading
        print("after read csv")
        # print basic info
        print("shape:", df.shape)
        print("columns:", list(df.columns))
        # print(df.head())
        print()
        print()
        print("-----------------------------------")
        # Example aggregation (guard against missing columns) (kind of unnecessary) 

        # Filter data for years 2010-2019
        recent_data = filter_deaths_by_year(df)
        
        # Simple for loop to assign columns to to_drop if they exist in df
        to_drop = [c for c in ['Entity', 'Code', 'Year'] if c in recent_data.columns]

        # If statement to check if to_drop is empty then performs drop and sum
        if to_drop:
            # Prints sum of numeric columns 
            print("sum of remaining numeric columns:")
            # Drop specified columns and sum the rest with a check for numeric only
            print(recent_data.drop(columns=to_drop).sum(numeric_only=True))
        else:
            # else is for error handling if no columns to drop
            print("No Entity/Code/Year columns to drop for aggregation")
    except Exception as e:
        print("Failed to read or process CSV:", e)
        raise


    #  Filter
def filter_deaths_by_year(df):
    recent_data  = df[(df["Year"] >= 2010) & (df["Year"] <= 2019)]
    return recent_data


def main():
    csv_path = Path(__file__).parent / "deaths_of_world.csv"
    print("before read csv")

    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}")
        sys.exit(1)
    print_file_general(csv_path)

if __name__ == "__main__":
    main()