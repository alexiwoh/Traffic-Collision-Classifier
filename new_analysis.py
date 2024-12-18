import pandas as pd
from visualization import *
from interpretability import *
from model import *
from imblearn.over_sampling import SMOTE
from metrics import *


def data_prep(df):
    """
    Main function to prepare the data by removing columns, 
    handling missing values, removing rows with 'Unknown' values, 
    and performing feature engineering.
    """

    # List of columns to drop.
    columns_to_drop = DATA_COLUMNS_TO_DROP

    df = remove_columns(df, columns_to_drop)  # Step 1: Remove unnecessary columns.

    df = check_missing_values(df)  # Step 2: Handle missing values.

    df = check_unknowns(df)  # Step 3: Remove rows with 'Unknown'.

    df = feature_engineering(df)  # Step 4: Extract new features from existing data.

    columns_to_drop = ["Accident_Date", "Accident_Time"]

    df = remove_columns(df, columns_to_drop)

    unique_columns = ["Location_Type", "Classification_Of_Accident", "Initial_Impact_Type", "Road_Surface_Condition",
                      "Environment_Condition", "Light", "Traffic_Control"]

    get_unique_values_to_excel(df, unique_columns, "Updated_Datasets/unique_cols_dataset.csv")

    # Specify the columns to process.
    columns_to_trim = [
        "Classification_Of_Accident",
        "Initial_Impact_Type",
        "Road_Surface_Condition",
        "Environment_Condition",
        "Light",
        "Traffic_Control"
    ]

    # Apply the function.
    df = trim_columns(df, columns_to_trim)

    get_unique_values_to_excel(df, columns_to_trim, "Updated_Datasets/unique_cols_dataset_after_trim.csv")

    # Visualize data insights
    visualize(df)

    df = columns_encoding(df)

    # Specify the output file name for the cleaned dataset.
    output_file = PATH_CLEANED_DATASET_OUTPUT

    # Write the updated DataFrame to a CSV file.
    df.to_csv(output_file, index=False, mode='w')

    print(f"\nCleaned dataset with engineered features has been written to {output_file}.")

    # Print the first few rows of the cleaned DataFrame.
    print("\nPreview of the cleaned dataset with new features:")
    print(df.head())

    return df


def remove_columns(df, columns_to_drop):
    """
    Removes unnecessary columns from the dataset.
    """

    # Drop the specified columns before any analysis.
    df = df.drop(columns=columns_to_drop)

    print("\nUnnecessary columns have been removed.")
    return df


def check_missing_values(df):
    """
    Identifies and removes rows with missing values.
    """

    # Check for missing values in the remaining columns.
    missing_values = df.isnull().sum()

    # Filter and display only columns with missing values.
    columns_with_missing = missing_values[missing_values > 0]
    print("\nColumns with missing values and their counts:")
    print(columns_with_missing)

    # Remove rows with missing values.
    rows_before = len(df)
    df = df.dropna()
    rows_after = len(df)

    print(f"\nRows with missing values removed: {rows_before - rows_after}")

    return df


def check_unknowns(df):
    """
    Identifies and removes rows where any value contains 'Unknown' (partial matches).
    """

    # Check for rows containing "Unknown" as part of the value.
    rows_before = len(df)

    # Remove rows with any cell containing the string 'Unknown'.
    df = df[~df.applymap(lambda x: "Unknown" in str(x)).any(axis=1)]

    rows_after = len(df)

    print(f"\nRows containing 'Unknown' removed: {rows_before - rows_after}")

    return df


def feature_engineering(df):
    """
    Extracts 'year', 'month', 'day', 'hour', and 'minute'.
    from the 'Accident_Date' and 'Accident_Time' columns.
    """

    # Ensure 'Accident_Date' and 'Accident_Time' columns are strings.
    df["Accident_Date"] = df["Accident_Date"].astype(str)
    df["Accident_Time"] = df["Accident_Time"].astype(str)

    # Extract year, month, and day from Accident_Date.
    df["year"] = df["Accident_Date"].apply(lambda x: x.split("/")[0])
    df["month"] = df["Accident_Date"].apply(lambda x: x.split("/")[1])
    df["day"] = df["Accident_Date"].apply(lambda x: x.split("/")[2])

    # Extract hour and minute from Accident_Time.
    df["hour"] = df["Accident_Time"].apply(lambda x: x.split(":")[0])
    df["minute"] = df["Accident_Time"].apply(lambda x: x.split(":")[1])

    print("\nFeature engineering completed. New features 'year', 'month', 'day', 'hour', and 'minute' have been added.")
    return df


def get_unique_values_to_excel(df, columns, output_file):
    """
    Get all unique values for the specified columns in the DataFrame and output them to an Excel file.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.
        columns (list): List of column names to get unique values from.
        output_file (str): Path to the Excel file where Results will be saved.

    Returns:
        None
    """
    unique_values = {}

    # Collect unique values for each column
    for column in columns:
        if column in df.columns:
            unique_values[column] = df[column].unique().tolist()
        else:
            print(f"Warning: Column '{column}' does not exist in the DataFrame.")
            unique_values[column] = []

    # Create a DataFrame where each column contains the unique values for that column
    unique_values_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in unique_values.items()]))

    # Output the unique values to an Excel file
    unique_values_df.to_csv(output_file, index=False)
    # print(f"Unique values have been written to {output_file}.")


def trim_columns(df, columns):
    """
    Trims the first 5 characters from the specified columns in a DataFrame,
    keeping only the string after the 5th character.

    Parameters:
        df (pd.DataFrame): The DataFrame to modify.
        columns (list): List of column names to trim.

    Returns:
        pd.DataFrame: The modified DataFrame with updated columns.
    """
    for col in columns:
        if col in df.columns:
            # Trim the first 5 characters from the column
            df[col] = df[col].apply(lambda x: x[5:] if isinstance(x, str) and len(x) > 5 else x)
        else:
            print(f"Warning: Column '{col}' does not exist in the DataFrame.")
    return df


def columns_encoding(df):
    # One-hot encode nominal columns
    nominal_columns = ["Location_Type", "Initial_Impact_Type", "Road_Surface_Condition", "Environment_Condition",
                       "Traffic_Control"]
    df = pd.get_dummies(df, columns=nominal_columns, drop_first=True)

    # Label encode ordinal columns
    ordinal_columns = {"Classification_Of_Accident": {"P.D. only": 0, "Non-fatal injury": 1, "Fatal injury": 2},
                       "Light": {"Dawn": 0, "Daylight": 1, "Dusk": 2, "Dark": 3, "Other": 4}}
    for col, mapping in ordinal_columns.items():
        df[col] = df[col].map(mapping)

    return df


def handle_class_imbalance(X, y):
    """
    Handles class imbalance using SMOTE (Synthetic Minority Oversampling Technique).

    Parameters:
        X: Feature matrix.
        y: Target vector.

    Returns:
        X_resampled, y_resampled: Balanced feature matrix and target vector.
    """
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    print("\nClass imbalance handled using SMOTE.")
    return X_resampled, y_resampled


def visualize_and_interpret(df, model, X):
    """
    Handles visualization and interpretability of the model and data.

    Parameters:
        df: The processed DataFrame.
        model: The trained Random Forest model.
        X: Feature matrix used for training.
    """
    # Plot feature importance
    plot_feature_importance(model, X.columns)

    # SHAP values for model interpretability
    explain_with_shap(model, X)

    # Generate partial dependence plots (PDPs)
    plot_pdp(model, X, X.columns)


def check_classification_type(y):
    """
    Determines whether the classification is binary or multi-class.

    Parameters:
        y: Target variable (Series or array).

    Returns:
        str: "Binary Classification" or "Multi-Class Classification".
    """
    num_classes = len(pd.Series(y).unique())
    if num_classes == 2:
        return "Binary Classification"
    else:
        return "Multi-Class Classification"


# Specify the path to your CSV file.
file_path = PATH_ORIGINAL_DATASET

# Load the CSV file into a DataFrame.
df = pd.read_csv(file_path)

# Apply data cleaning and pre-processing functions.
df = data_prep(df)

# Verify successful cleaning.
print(f"\nFinal number of rows in the cleaned dataset: {len(df)}")

# Split into features and target variables.
X, y = split_features_target(df, "Classification_Of_Accident")

# Handle class imbalance.
X_resampled, y_resampled = handle_class_imbalance(X, y)

# Example usage
classification_type = check_classification_type(y_resampled)
print(f"The task is: {classification_type}")

# Train the Random Forest Classifier.
model, y_test, y_pred, y_pred_proba = train_random_forest(X_resampled, y_resampled)

# Class names for visualization
class_names = df["Classification_Of_Accident"].unique()

# Example usage
# Metrics visualization
plot_confusion_matrix(y_test, y_pred, class_names)
plot_multiclass_roc_curve(y_test, y_pred_proba, class_names)
plot_multiclass_precision_recall_curve(y_test, y_pred_proba, class_names)
plot_feature_importance_bar(model, X.columns)
plot_classification_report(y_test, y_pred)
plot_misclassifications(y_test, y_pred)

# Visualize and create interpretability insights.
# visualize_and_interpret(df, model, X_resampled)
