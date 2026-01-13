import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1 function
def filter_deaths_by_year(df):
    """Filter data for years 2010-2019."""
    recent_data = df[(df["Year"] >= 2010) & (df["Year"] <= 2019)]
    return recent_data

# 2 function
def group_by_code(recent_data, top_n=15):
    """Aggregate total deaths per country code and keep the top N."""
    totals = (
        recent_data.groupby("Code")["Total Deaths"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    return totals

# 3 function
def print_file_general(csv_path):
    """Read and analyze deaths data from CSV file."""
    print(f"CSV file found at: {csv_path}")
    print(f"File size: {csv_path.stat().st_size} bytes")
    print("--------------------------------")

    # Read CSV file with error handling
    df = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
    
    print("CSV loaded successfully")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("-----------------------------------\n")

    # Filter data for years 2010-2019
    recent_data = filter_deaths_by_year(df)
    
    # Calculate total deaths per row; exclude id columns and any existing total to avoid double counting
    cause_columns = [
        c for c in recent_data.columns
        if c not in ["Entity", "Code", "Year", "Total Deaths"]
    ]
    recent_data["Total Deaths"] = recent_data[cause_columns].sum(axis=1, numeric_only=True)

    top_by_code = group_by_code(recent_data)

    print("\nHighest Total Deaths per Country Code (top 15):")
    print(top_by_code)
    print("What are the top 15 country codes with the highest total deaths from 2010 to 2019?")
    print("\n")
    plot_deaths(top_by_code)

def plot_deaths(top_by_code):
    top_by_code.plot(
        x="Code",
        y="Total Deaths",
        kind="bar",
        color='red',
        title="Highest Total Deaths by Country Code (2010-2019)",
        legend=False,
        figsize=(12, 6)
    )
    plt.title("Highest Total Deaths by Country Code (2010-2019)")
    plt.xlabel("Country Code")
    plt.ylabel("Total Deaths")
    plt.tight_layout()
    plt.show()

# 4 main function
def main():
    """Main function to load and process deaths data."""
    csv_path = Path(__file__).parent / "deaths_of_world.csv"
    
    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}")
        sys.exit(1)
    
    print_file_general(csv_path)


if __name__ == "__main__":
    main()