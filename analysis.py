import pandas as pd

# Specify the path to your CSV file
file_path = "Datasets/Traffic_Collision_Dataset.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# List of columns to drop
columns_to_drop = [
    "ObjectId",
    "Num_of_Fatal_Injuries",
    "Num_of_Major_Injuries",
    "Num_Of_Pedestrians",
    "Num_of_Bicycles",
    "Num_of_Motorcycles",
    "Max_Injury",
    "Num_of_Injuries",
    "Num_of_Minimal_Injuries",
    "Num_of_Minor_Injuries",
    "Accident_Year",
    "Geo_ID",
    "ID",
    "X",
    "Y",
    "X_Coordinate",
    "Y_Coordinate",
    "Location", 
    "Num_of_Vehicle"
]

# Drop the specified columns before any analysis
df = df.drop(columns=columns_to_drop)

# Check for missing values in the remaining columns
missing_values = df.isnull().sum()

# Filter and display only columns with missing values
columns_with_missing = missing_values[missing_values > 0]
print("Columns with missing values and their counts:")
print(columns_with_missing)

# Identify rows with missing values
rows_with_missing = df[df.isnull().any(axis=1)]

# Export rows with missing values to an Excel file
missing_rows_file = "Updated_Datasets/missing_rows.csv"
rows_with_missing.to_csv(missing_rows_file, index=False)
print(f"Rows with missing values have been saved to {missing_rows_file}.")



# Check for rows containing "Unknown" as part of the value
unknown_counts = df.applymap(lambda x: "Unknown" in str(x)).sum()  # Count occurrences of "Unknown" in each column
unknown_total = unknown_counts.sum()  # Total occurrences across the dataset

# Filter columns that contain "Unknown"
columns_with_unknown = unknown_counts[unknown_counts > 0]

# Display results
print("\nColumns containing 'Unknown' (partial matches included) and their counts:")
print(columns_with_unknown)

print(f"\nTotal rows containing 'Unknown' (partial matches included): {unknown_total}")
