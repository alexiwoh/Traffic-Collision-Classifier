import pandas as pd
from constants import *
from helpers import *
from new_analysis import df as data


def summary_statistics(data_frame):
    def func():
        for feature in DATA_FINAL_FEATURES:
            print(data_frame[feature].describe())
            print("----")

    run_section(TITLE_SUMMARY_STATISTICS, func)


def visualizations(data_frame):
    print(data_frame)


if __name__ == '__main__':
    summary_statistics(data)
