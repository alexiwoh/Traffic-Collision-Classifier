# File Paths
PATH_ORIGINAL_DATASET = "Datasets/Traffic_Collision_Dataset.csv"
PATH_CLEANED_DATASET_OUTPUT = "Updated_Datasets/cleaned_dataset.csv"

# Titles
TITLE_LENGTH = 42
TITLE_SUMMARY_STATISTICS = "SUMMARY STATISTICS"

#  Data constants

DATA_FINAL_FEATURES = [
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
    "minute"
]

# List of columns to drop
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
    "X",
    "Y",
    "X_Coordinate",
    "Y_Coordinate",
    "Location",
    "Num_of_Vehicle"
]
