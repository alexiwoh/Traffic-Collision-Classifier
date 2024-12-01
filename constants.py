"""
This file contains all shared constants.
"""

# File Paths
PATH_ORIGINAL_DATASET = "Datasets/Traffic_Collision_Dataset.csv"
PATH_CLEANED_DATASET_OUTPUT = "Updated_Datasets/cleaned_dataset.csv"
PATH_VISUALIZATIONS = "Visualizations"
PATH_RESULTS = "Results"

# Titles and text.
TITLE_LENGTH = 42
DIVIDER_LENGTH = 10
TITLE_SUMMARY_STATISTICS = "SUMMARY STATISTICS"

# Stylistic constants.
VISUALIZATIONS_FILE_TYPE = ".png"

#  Dataset related constants
# Final features to be used for analysis.
FEATURE_LOCATION = "Location"
DATA_FINAL_FEATURES = [
    FEATURE_LOCATION,
    "Location_Type",
    "Classification_Of_Accident",
    "Initial_Impact_Type",
    "Road_Surface_Condition",
    "Environment_Condition",
    "Light",
    "Traffic_Control",
    "Lat",
    "Long",
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "X",
    "Y",
    "X_Coordinate",
    "Y_Coordinate",
]

# List of final categorical features being used.
DATA_CATEGORICAL_FEATURES = [
    "Location_Type",
    "Classification_Of_Accident",
    "Initial_Impact_Type",
    "Road_Surface_Condition",
    "Environment_Condition",
    "Light",
    "Traffic_Control",
]

# List of final numerical features being used.
DATA_NUMERICAL_FEATURES = [
    "Lat",
    "Long",
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "X",
    "Y",
    "X_Coordinate",
    "Y_Coordinate",
]

# Dictionary for month mapping.
MONTH_MAPPING = {
    "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June",
    "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"
}

# List of columns to drop.
DATA_COLUMNS_TO_DROP = [
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
    "Num_of_Vehicle"
]
