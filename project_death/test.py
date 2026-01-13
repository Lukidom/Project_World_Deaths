```python
import sys  # Import system-specific parameters and functions
from pathlib import Path  # Import Path for file path handling
import pandas as pd  # Import pandas for data manipulation
import matplotlib.pyplot as plt  # Import matplotlib for plotting

# 1 function
def filter_deaths_by_year(df):
    """Filter data for years 2010-2019."""
    recent_data = df[(df["Year"] >= 2010) & (df["Year"] <= 2019)]  # Keep only rows where Year is between 2010 and 2019
    return recent_data  # Return the filtered DataFrame

# 2 function
def group_by_code(recent_data):
    """Get highest total deaths per country code."""
    result = recent_data.loc[recent_data.groupby("Code")["Total Deaths"].idxmax()]  # For each Code, find the row with the highest Total Deaths
    result = result.sort_values(by="Total Deaths", ascending=False)  # Sort the resulting rows by Total Deaths descending
    return result  # Return the sorted DataFrame

# 3 function
def print_file_general(csv_path):
    """Read and analyze deaths data from CSV file."""
    print(f"CSV file found at: {csv_path}")  # Print the file path
    print(f"File size: {csv_path.stat().st_size} bytes")  # Print the file size in bytes
    print("--------------------------------")  # Separator for readability

    # Read CSV file with error handling
    df = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')  # Load CSV into a DataFrame, skip bad lines
    
    print("CSV loaded successfully")  # Confirm CSV loaded
    print(f"Shape: {df.shape}")  # Print number of rows and columns
    print(f"Columns: {list(df.columns)}")  # Print the column names
    print("-----------------------------------\n")  # Separator for readability

    # Filter data for years 2010-2019
    recent_data = filter_deaths_by_year(df)  # Call function to filter recent years
    
    # Calculate total deaths per row
    to_drop = [c for c in ['Entity', 'Code', 'Year'] if c in recent_data.columns]  # Determine non-numeric columns to drop for summing
    recent_data["Total Deaths"] = recent_data.drop(columns=to_drop).sum(axis=1, numeric_only=True)  # Sum numeric columns left-to-right per row
    
    # Display results
    print("Total Deaths by Country Code (2010-2019):")  # Print header
    print(recent_data[["Code", "Total Deaths"]])  # Print Code and calculated Total Deaths
    
    top_by_code = group_by_code(recent_data)  # Get the row with the highest total deaths per Code
    print("\nHighest Total Deaths per Country Code:")  # Print header
    print(top_by_code)  # Print the top rows
    
    plot_deaths(top_by_code)  # Call plotting function to visualize the results

def plot_deaths(top_by_code):
    top_by_code.plot(
        x="Code",  # Use 'Code' column for x-axis
        y="Total Deaths",  # Use 'Total Deaths' column for y-axis
        kind="bar",  # Plot as a bar chart
        title="Highest Total Deaths by Country Code (2010-2019)",  # Set chart title
        legend=False,  # Hide the legend
        figsize=(10, 6)  # Set figure size
    )
    plt.title("Highest Total Deaths by Country Code (2010-2019)")  # Set the title again for matplotlib
    plt.xlabel("Country Code")  # Label x-axis
    plt.ylabel("Total Deaths")  # Label y-axis
    plt.tight_layout()  # Adjust layout to prevent label overlap
    plt.show()  # Display the plot

# 4 main function
def main():
    """Main function to load and process deaths data."""
    csv_path = Path(__file__).parent / "deaths_of_world.csv"  # Set the CSV file path relative to this script
    
    if not csv_path.exists():  # Check if the file exists
        print(f"ERROR: CSV not found at {csv_path}")  # Print error if file missing
        sys.exit(1)  # Exit the program
    
    print_file_general(csv_path)  # Call main processing function

if __name__ == "__main__":
    main()  # Run main function when script is executed
```
