'''
Luke Ramirez
Projeect #1
deaths_of_world.py
Project Death - Analyze global deaths data from CSV
'''
# Setup 
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import logging as log
import time as time

# 1 function
'''Filter data for years 2010-2019.'''
def filter_deaths_by_year(df):
    recent_data = df[(df["Year"] >= 2010) & (df["Year"] <= 2019)] # Filter for years 2010-2019
    return recent_data

# 2 function
'''Get highest total deaths per country code'''
def group_by_code(recent_data, top_n=15):
    # Error handling: Validate input parameters
    if recent_data.empty:
        log.error("Input data is empty")
        return pd.DataFrame()  # Return empty DataFrame
    
    totals = (
        recent_data.groupby("Code")["Total Deaths"] # Group by country code
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    return totals

# 3 function
'''Get total deaths by year'''
def group_by_year(recent_data):
    totals = (recent_data.groupby("Year")["Total Deaths"] # Group by year
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return totals

    
# 4 function
'''Read and analyze deaths data from CSV file.'''
def print_file_general(csv_path):

    print(f"CSV file found at: {csv_path}")
    print(f"File size: {csv_path.stat().st_size} bytes") # File size
    print("--------------------------------")

    # Read CSV file with error handling
    try:
        df = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip') # Read CSV with latin1 encoding and skip bad lines
    except FileNotFoundError:
        print(f"ERROR: File not found at {csv_path}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("ERROR: CSV file is empty")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to read CSV file: {e}")
        sys.exit(1)
    
    print("CSV loaded successfully")
    print(f"Shape: {df.shape}") # DataFrame shape
    print(f"Columns: {list(df.columns)}") # List of columns
    print("-----------------------------------\n")
    
    # Error handling: Validate required columns exist
    required_columns = ["Code", "Year"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"ERROR: Missing required columns: {missing_columns}")
        sys.exit(1)

    # Filter data for years 2010-2019
    recent_data = filter_deaths_by_year(df) # Filter for recent years
    
    # Calculate total deaths per row; exclude id columns and any existing total to avoid double counting
    cause_columns = [
        c for c in recent_data.columns # Identify cause columns
        if c not in ["Entity", "Code", "Year", "Total Deaths"]
    ]
    recent_data["Total Deaths"] = recent_data[cause_columns].sum(axis=1, numeric_only=True) # Sum cause columns to get total deaths per row

    top_by_code = group_by_code(recent_data) # Get top 15 country codes by total deaths

    print("\nHighest Total Deaths per Country Code (top 15):")
    print(top_by_code)
    print("What are the top 15 country codes with the highest total deaths from 2010 to 2019?")
    print("\n")
    plot_deaths(top_by_code) # Plot the top 15 country codes by total deaths

    totals_by_year = group_by_year(recent_data) # Get total deaths by year
    print("\nTotal Deaths by Year (2010-2019):")
    print(totals_by_year)
    plot_deaths_by_year(totals_by_year) # Plot total deaths by year


    # 5 function
'''Plot total deaths by country code'''
def plot_deaths(top_by_code):# Plot total deaths by country code
    # Error handling: Validate data before plotting
    if top_by_code.empty:
        print("ERROR: No data to plot")
        return
    
    try:
        top_by_code.plot(
            x="Code",
            y="Total Deaths",
            kind="bar",
            color='green',
            title="Highest Total Deaths by Country Code (2010-2019)",
            legend=False,
            figsize=(12, 6)
        )
        plt.title("Highest Total Deaths by Country Code (2010-2019) Top 15")
        plt.xlabel("Country Code")
        plt.ylabel("Total Deaths")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"ERROR: Failed to create plot: {e}")
        return


    # 6 function
'''Plot total deaths by year'''
def plot_deaths_by_year(totals_by_year):# Plot total deaths by year
    
    time.sleep(5)  # Pause for 1 second before plotting
    if totals_by_year.empty:
        print("ERROR: No data to plot")
        return
    
    try:
        totals_by_year.plot(
            x="Year",
            y="Total Deaths",
            kind="line",
            marker='o',
            color='blue',
            title="Total Deaths by Year (2010-2019)",
            legend=False,
            figsize=(10, 5)
        )
        plt.title("Total Deaths by Year (2010-2019)")
        plt.xlabel("Year")
        plt.ylabel("Total Deaths")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"ERROR: Failed to create plot: {e}")
        return

# main function
    """Main function to load and process deaths data."""
def main():
    csv_path = Path(__file__).parent / "deaths_of_world.csv" # Path to CSV file
    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}")
        sys.exit(1)
    print_file_general(csv_path)


if __name__ == "__main__":
    main()