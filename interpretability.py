import os
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay
from constants import *
import shap


def plot_feature_importance(model, feature_names):
    """
    Plots the feature importance from a trained Random Forest model.

    Parameters:
        model: Trained Random Forest model.
        feature_names (list): List of feature names.
    """
    importances = model.feature_importances_
    indices = importances.argsort()[::-1]  # Sort in descending order
    sorted_features = [feature_names[i] for i in indices]

    # Plot the feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(sorted_features, importances[indices], align="center", color="skyblue")
    title = "Feature Importance"
    plt.title(title)
    plt.xlabel("Importance")
    plt.ylabel("Features")
    plt.gca().invert_yaxis()
    plt.savefig(os.path.join(PATH_RESULTS, f"{title}{VISUALIZATIONS_FILE_TYPE}"))
    plt.close()


def explain_with_shap(model, X):
    """
    Explains the Random Forest predictions using SHAP.

    Parameters:
        model: Trained Random Forest model.
        X: Feature matrix (DataFrame).
    """
    # Initialize the SHAP Tree Explainer
    explainer = shap.TreeExplainer(model)

    # Compute SHAP values
    shap_values = explainer.shap_values(X)

    # Global interpretability: Summary plot
    print("Global Interpretability (SHAP Summary Plot):")
    shap.summary_plot(shap_values[1], X, plot_type="bar")  # For classification, use shap_values[1]

    # Local interpretability: Force plot for a single prediction
    print("Local Interpretability (Example Force Plot):")
    shap.force_plot(explainer.expected_value[1], shap_values[1][0], X.iloc[0], matplotlib=True)


def plot_pdp(model, X, feature_names):
    """
    Plots Partial Dependence Plots (PDPs) for selected features.

    Parameters:
        model: Trained Random Forest model.
        X: Feature matrix (DataFrame).
        feature_names (list): List of feature names to analyze.
    """
    # Select features to visualize
    selected_features = [0, 1]  # Indexes of features to plot (adjust based on your features)

    # Generate Partial Dependence Plots
    PartialDependenceDisplay.from_estimator(
        model, X, selected_features, feature_names=feature_names, grid_resolution=50
    )
    plt.savefig(os.path.join(PATH_RESULTS, f"Partial Dependence Plot{VISUALIZATIONS_FILE_TYPE}"))
    plt.close()
