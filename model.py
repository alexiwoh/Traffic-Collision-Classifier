from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd


def split_features_target(df, target_column):
    """
    Splits a DataFrame into features (X) and target (y).

    Parameters:
        df (pd.DataFrame): The DataFrame to split.
        target_column (str): The column name to use as the target (y).

    Returns:
        tuple: A tuple containing:
            - X (pd.DataFrame): The features DataFrame.
            - y (pd.Series): The target column as a Series.
    """
    if target_column not in df.columns:
        raise ValueError(f"Column '{target_column}' not found in the DataFrame.")

    # Features (X) exclude the target column
    X = df.drop(columns=[target_column])

    # Target (y) is the specified column
    y = df[target_column]

    return X, y


def class_distribution(y):
    """
    Calculates and prints the distribution of class labels.

    Parameters:
        y (pd.Series or np.array): The target variable (class labels).

    Returns:
        pd.DataFrame: A DataFrame showing class counts and percentages.
    """

    # Calculate class counts
    counts = pd.Series(y).value_counts()

    # Calculate percentages
    percentages = pd.Series(y).value_counts(normalize=True) * 100

    # Combine counts and percentages into a DataFrame
    distribution = pd.DataFrame({
        "Count": counts,
        "Percentage": percentages
    })

    return distribution


def train_random_forest(X, y, test_size=0.3, random_state=42, n_estimators=100):
    """
    Trains a Random Forest Classifier on the given features (X) and target (y).

    Parameters:
        X (pd.DataFrame or np.array): Feature matrix.
        y (pd.Series or np.array): Target vector.
        test_size (float): Proportion of the dataset to include in the test split. Default is 0.3.
        random_state (int): Random seed for reproducibility. Default is 42.
        n_estimators (int): Number of trees in the forest. Default is 100.

    Returns:
        tuple: A tuple containing:
            - model: Trained Random Forest Classifier.
            - y_test: True labels for the test set.
            - y_pred: Predicted labels for the test set.
    """
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Initialize the Random Forest Classifier
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Get predicted probabilities for all classes
    y_pred_proba = model.predict_proba(X_test)

    # Print evaluation metrics
    print("Model Performance:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model, y_test, y_pred, y_pred_proba
