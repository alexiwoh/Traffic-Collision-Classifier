from helpers import *
from new_analysis import df as data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def summary_statistics(data_frame=data, features: list = DATA_FINAL_FEATURES):
    def func():
        for feature in features:
            print(data_frame[feature].describe(include="all"))
            if feature in DATA_CATEGORICAL_FEATURES:
                print(data_frame[feature].value_counts())
            print_divider()

    run_section(TITLE_SUMMARY_STATISTICS, func)


def visualize_bar_plots(data_frame=data, features: list[str] = DATA_CATEGORICAL_FEATURES):
    for feature in features:
        # Count the occurrences of each category and sort them.
        sorted_counts = data_frame[feature].value_counts().sort_values(ascending=False)

        # Convert the sorted index to a categorical type for ordering in the plot.
        data_frame[feature] = pd.Categorical(data_frame[feature], categories=sorted_counts.index, ordered=True)

        # Create the count plot.
        feature_name = feature.replace("_", " ")
        title = f"Accidents by {feature_name}"
        plt.figure(figsize=(10, 6))  # Set figure size for better resolution
        sns.countplot(data=data_frame, x=feature, order=sorted_counts.index)
        plt.title(title)
        plt.xlabel(feature_name)
        plt.ylabel('Number of Accidents')
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability

        # Save the plot to a file.
        plt.savefig(f"{PATH_VISUALIZATIONS}{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches='tight')


def visualizations(data_frame):
    summary_statistics(data_frame, DATA_FINAL_FEATURES)
    visualize_bar_plots(data_frame, DATA_CATEGORICAL_FEATURES)


if __name__ == '__main__':
    visualizations(data)

