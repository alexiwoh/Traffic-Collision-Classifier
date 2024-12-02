import textwrap

from helpers import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def summary_statistics(data_frame, features: list = DATA_FINAL_FEATURES):
    """
    Summary stats for data frame.
    :param data_frame: the data frame.
    :param features: features to summarize.
    :return:
    """

    def func():
        for feature in features:
            print(data_frame[feature].describe(include="all"))
            if feature in DATA_CATEGORICAL_FEATURES:
                print(data_frame[feature].value_counts())
            print_divider()

    run_section(TITLE_SUMMARY_STATISTICS, func)


def visualize_bar_plots(data_frame, features: list[str] = DATA_CATEGORICAL_FEATURES, stack_plots: bool = False):
    """
    Creates bar plots of categorical features.
    """
    if stack_plots:
        # Create stacked plots for each pair of features.
        # Store stacked plots information in a dictionary.
        plots = {}

        for feature1 in features:
            for feature2 in features:
                if feature1 == feature2:
                    continue

                crosstab_result = pd.crosstab(data_frame[feature1], data_frame[feature2])

                # Sort the columns of crosstab_result based on their total sum in descending order
                crosstab_result = crosstab_result[sorted(crosstab_result.columns,
                                                         key=lambda col: crosstab_result[col].sum(),
                                                         reverse=True)]

                # Sort the index of crosstab_result by its total sum in descending order
                crosstab_result = crosstab_result.loc[sorted(crosstab_result.index,
                                                             key=lambda row: crosstab_result.loc[row].sum(),
                                                             reverse=True)]

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
            plt.savefig(f"{PATH_VISUALIZATIONS}/Stacked Bar Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300,
                        bbox_inches="tight")
            plt.close()
    else:
        for feature in features:
            # Count the occurrences of each category and sort them.
            sorted_counts = data_frame[feature].value_counts().sort_values(ascending=False)

            # Convert the sorted index to a categorical type for ordering in the plot.
            temp_feature = feature + "_temp"
            data_frame[temp_feature] = pd.Categorical(data_frame[feature], categories=sorted_counts.index, ordered=True)

            # Create the count plot.
            feature_name = feature.replace("_", " ")
            title = f"Bar Plot of Accidents by {feature_name}"
            plt.figure(figsize=(10, 6))  # Set figure size for better resolution
            sns.countplot(data=data_frame, x=temp_feature, order=sorted_counts.index)
            plt.title(title)
            plt.xlabel(feature_name)
            plt.ylabel("Number of Accidents")
            plt.xticks(rotation=45)  # Rotate x-axis labels for readability

            # Save the plot to a file.
            plt.savefig(f"{PATH_VISUALIZATIONS}/Bar Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300,
                        bbox_inches="tight")
            plt.close()

            data_frame.drop(columns=[temp_feature], inplace=True)


def visualize_geographic_data(data_frame):
    """
    Scatter Plots for geographical data.
    """

    """ 
        Scatterplot for longitude vs latitude of accidents.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(data_frame["Long"], data_frame["Lat"], alpha=0.5)
    title = "Latitude vs Longitude of Accidents"
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.xticks(rotation=45)
    # Save the plot to a file.
    plt.savefig(f"{PATH_VISUALIZATIONS}/Scatter Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
    plt.close()

    """ 
        Scatterplot Map for longitude vs latitude of accidents.
    """
    plt.figure(figsize=(10, 6))

    # Create a Basemap instance with Mercator projection
    filtered_data = data_frame[(data_frame["Lat"] > 43) & (data_frame["Long"] > -77)]
    m = Basemap(projection='merc', llcrnrlat=min(filtered_data["Lat"]), urcrnrlat=max(filtered_data["Lat"]),
                llcrnrlon=min(filtered_data["Long"]), urcrnrlon=max(filtered_data["Long"]), resolution='i')
    # Draw map features (optional)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    # Convert longitude and latitude to map projection coordinates
    x, y = m(data_frame["Long"].values, data_frame["Lat"].values)
    # Plot scatter on the map (on top of the background)
    m.scatter(x, y, color='red', edgecolor='black', linewidth=1, alpha=0.5, marker='o')

    title = "Map of Latitude vs Longitude of Accidents"
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.xticks(rotation=45)
    plt.savefig(f"{PATH_VISUALIZATIONS}/Scatter Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
    plt.close()

    """
        Scatterplot for X vs Y of accidents.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(data_frame["X"], data_frame["Y"], alpha=0.5)
    title = "Y vs X of Accidents"
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.xticks(rotation=45)
    # Save the plot to a file.
    plt.savefig(f"{PATH_VISUALIZATIONS}/Scatter Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
    plt.close()

    """
        Bar Plot of the Top accident locations.
    """
    N = 10  # Number of locations.
    sorted_counts = data_frame[FEATURE_LOCATION].value_counts().sort_values(ascending=False)  # Count the occurrences and sort them.
    top_locations = sorted_counts.head(N)  # Extract the top N locations.
    top_indexes = top_locations.index.tolist()
    plt.figure(figsize=(N, 8))
    sns.barplot(
        x=top_indexes,
        y=top_locations.values,
        legend="full",
        hue=top_indexes,  # Add this to enable legend coloring
        dodge=False,  # Prevent separation of bars due to hue
        palette=f"tab{N}"  # Choose a colormap
    )
    plt.legend(title="Locations", bbox_to_anchor=(1.05, 1), loc='upper left')
    title = f"Bar Plot of Accidents at Top {N} Locations"
    plt.title(title)
    plt.xlabel(FEATURE_LOCATION)
    plt.ylabel("Number of Accidents")
    plt.xticks([])  # Remove x-tick labels since we will have a legend.
    plt.savefig(f"{PATH_VISUALIZATIONS}/Bar Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
    plt.close()

    data_frame.drop(columns=[FEATURE_LOCATION], inplace=True)  # Drop the Location column.


def visualize_time_plots(data_frame):
    """
    Bar plots for times.
    """
    features = ["year", "month", "hour"]
    for feature in features:
        plt.figure(figsize=(10, 6))

        # Establish numerical ordering.
        if feature == "hour":
            ordering = [str(n) for n in sorted([int(x) for x in data_frame[feature].unique()])]
        else:
            ordering = sorted(data_frame[feature].unique())

        # If the feature is "month", map it to the month names.
        if feature == "month":
            data_frame["month_name"] = data_frame["month"].map(MONTH_MAPPING)
            sns.countplot(x="month_name", data=data_frame, order=list(MONTH_MAPPING.values()))
        else:
            sns.countplot(x=feature, data=data_frame, order=ordering)

        title = f"Bar Plot of Accidents by {feature.capitalize()}"
        plt.title(title)
        plt.xlabel(f"{feature.capitalize()}")
        plt.ylabel("Number of Accidents")
        plt.xticks(rotation=45)
        plt.savefig(f"{PATH_VISUALIZATIONS}/Bar Plots/{title}{VISUALIZATIONS_FILE_TYPE}", dpi=300, bbox_inches="tight")
        plt.close()

        if feature == "month":
            data_frame.drop(columns=["month_name"], inplace=True)


def visualize(data_frame):
    """
    Produce statistics summary and visualization files.
    """
    print("<<<Starting Visualization>>>")
    summary_statistics(data_frame, DATA_FINAL_FEATURES)
    visualize_geographic_data(data_frame)
    visualize_time_plots(data_frame)
    visualize_bar_plots(data_frame, DATA_CATEGORICAL_FEATURES, stack_plots=False)
    visualize_bar_plots(data_frame, DATA_CATEGORICAL_FEATURES, stack_plots=True)
