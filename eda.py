from helpers import *
from new_analysis import df as data


def summary_statistics(data_frame):
    def func():
        for feature in DATA_FINAL_FEATURES:
            print(data_frame[feature].describe(include="all"))
            if feature in DATA_CATEGORICAL_FEATURES:
                print(data_frame[feature].value_counts())
            print_divider()

    run_section(TITLE_SUMMARY_STATISTICS, func)


def visualizations(data_frame):
    print(data_frame)


if __name__ == '__main__':
    summary_statistics(data)
