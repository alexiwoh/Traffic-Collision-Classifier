import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, roc_curve, auc, precision_recall_curve, classification_report
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import label_binarize
import os

# Create results directory if not exists
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_confusion_matrix(y_test, y_pred, class_names):
    disp = ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=class_names, cmap='Blues')
    disp.ax_.set_title("Confusion Matrix")
    plt.savefig(os.path.join(RESULTS_DIR, "confusion_matrix.png"))
    plt.show()

def plot_multiclass_roc_curve(y_test, y_pred_proba, class_names):
    y_test_binarized = label_binarize(y_test, classes=range(len(class_names)))
    plt.figure(figsize=(10, 7))
    
    for i, class_name in enumerate(class_names):
        fpr, tpr, _ = roc_curve(y_test_binarized[:, i], y_pred_proba[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=2, label=f"Class {class_name} (AUC = {roc_auc:.2f})")

    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Multi-Class ROC Curve")
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(RESULTS_DIR, "multiclass_roc_curve.png"))
    plt.show()

def plot_multiclass_precision_recall_curve(y_test, y_pred_proba, class_names):
    y_test_binarized = label_binarize(y_test, classes=range(len(class_names)))
    plt.figure(figsize=(10, 7))

    for i, class_name in enumerate(class_names):
        precision, recall, _ = precision_recall_curve(y_test_binarized[:, i], y_pred_proba[:, i])
        plt.plot(recall, precision, lw=2, label=f"Class {class_name}")

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Multi-Class Precision-Recall Curve")
    plt.legend(loc="lower left")
    plt.savefig(os.path.join(RESULTS_DIR, "multiclass_precision_recall_curve.png"))
    plt.show()

def plot_feature_importance_bar(model, feature_names):
    importances = model.feature_importances_
    indices = importances.argsort()[::-1]
    sorted_features = [feature_names[i] for i in indices]

    plt.figure(figsize=(10, 6))
    plt.barh(sorted_features, importances[indices], align='center', color='skyblue')
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Features')
    plt.gca().invert_yaxis()
    plt.savefig(os.path.join(RESULTS_DIR, "feature_importance.png"))
    plt.show()

def plot_classification_report(y_test, y_pred):
    report = classification_report(y_test, y_pred, output_dict=True)
    df_report = pd.DataFrame(report).transpose()

    plt.figure(figsize=(10, 6))
    sns.heatmap(df_report.iloc[:-1, :-1], annot=True, cmap="Blues", fmt=".2f")
    plt.title("Classification Report Heatmap")
    plt.savefig(os.path.join(RESULTS_DIR, "classification_report.png"))
    plt.show()

def plot_misclassifications(y_test, y_pred):
    misclassified = y_test != y_pred
    misclass_counts = pd.Series(y_test[misclassified]).value_counts()

    plt.figure(figsize=(8, 5))
    misclass_counts.plot(kind='bar', color='coral')
    plt.title("Misclassification Counts by Class")
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.savefig(os.path.join(RESULTS_DIR, "misclassifications.png"))
    plt.show()
