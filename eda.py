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


def visualize_bar_plots(data_frame=data, features: list[str] = DATA_CATEGORICAL_FEATURES, stack_plots: bool = False):
    """
    Creates bar plots of categorical features.
    """
    if stack_plots:
        # Create stacked plots for each pair of features.
        # Store stacked plots information in a dictionary.
        plots = {}

        for i, feature1 in enumerate(features):
            for feature2 in features[i + 1:]:  # Avoid self-comparison.
                crosstab_result = pd.crosstab(data_frame[feature1], data_frame[feature2])
                plots[(feature1, feature2)] = crosstab_result  # Store the stacked plot in the dictionary.

        # Plot as a stacked bar chart
        for (feature1, feature2), plot in plots.items():
            plot.plot(kind="bar", stacked=True, figsize=(10, 6))
            feature1, feature2 = feature1.replace("_", " "), feature2.replace("_", " ")
            title = f"Stacked Bar Plot of {feature1} vs {feature2}"
            plt.title(title)
            plt.xlabel(feature1)
            plt.ylabel("Number of Accidents")
            plt.xticks(rotation=45)

            # Save the plot to a file.
            plt.savefig(f"{PATH_VISUALIZATIONS}/Stacked Bar Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
            plt.close()
    else:
        for feature in features:
            # Count the occurrences of each category and sort them.
            sorted_counts = data_frame[feature].value_counts().sort_values(ascending=False)

            # Convert the sorted index to a categorical type for ordering in the plot.
            data_frame[feature] = pd.Categorical(data_frame[feature], categories=sorted_counts.index, ordered=True)

            # Create the count plot.
            feature_name = feature.replace("_", " ")
            title = f"Bar Plot of Accidents by {feature_name}"
            plt.figure(figsize=(10, 6))  # Set figure size for better resolution
            sns.countplot(data=data_frame, x=feature, order=sorted_counts.index)
            plt.title(title)
            plt.xlabel(feature_name)
            plt.ylabel("Number of Accidents")
            plt.xticks(rotation=45)  # Rotate x-axis labels for readability

            # Save the plot to a file.
            plt.savefig(f"{PATH_VISUALIZATIONS}/Bar Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
            plt.close()


def visualizations(data_frame):
    summary_statistics(data_frame, DATA_FINAL_FEATURES)
    visualize_bar_plots(data_frame, DATA_CATEGORICAL_FEATURES, stack_plots=False)
    visualize_bar_plots(data_frame, DATA_CATEGORICAL_FEATURES, stack_plots=True)


if __name__ == '__main__':
    visualizations(data)
