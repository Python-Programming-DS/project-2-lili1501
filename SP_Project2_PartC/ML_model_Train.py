"""
Training ML model for Tic Tac Toe game
> Description:
Using HistGradientBoostingClassifier to train a model to predict the best move 
for the computer (O) in Tic Tac Toe game

By: Shesadree Priyadarshani

"""

# Importing necessary libraries for ML model training and evaluation
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn import metrics
from sklearn.model_selection import  RandomizedSearchCV
from sklearn.metrics import roc_auc_score
import joblib

# Reading the tictac_single.txt file using pandas
# Getting the current directory of the script to avoid path issues
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'tictac_single.txt')
print(f"File path: {file_path}")

tictac_df = pd.read_csv(file_path, sep=" ", header=None)
X = tictac_df.iloc[:, :-1]
y = tictac_df.iloc[:, -1]

# Training the ML model using RandomForestClassifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
hgb = HistGradientBoostingClassifier(random_state=42)
hgb.fit(X_train, y_train)
y_pred = hgb.predict(X_test)

# Hyperparameter tuning using RandomizedSearchCV
param_grid_hgb = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_iter': [100, 200, 300],
    'max_depth': [None, 5, 10],
    'min_samples_leaf': [10, 20, 30],
    'l2_regularization': [0.0, 0.1, 0.5, 1.0],
    'early_stopping': [True, False]
    }

grid = RandomizedSearchCV(
    estimator=hgb,
    param_distributions=param_grid_hgb,
    n_iter=20,
    cv=3,                   
    scoring='f1_weighted',
    )

grid.fit(X_train, y_train)

print("Best parameters:", grid.best_params_)
print("Best CV Score:", grid.best_score_)


best_model = grid.best_estimator_

# Saving the best model using joblib to avoid retraining every time
joblib.dump(best_model, 'SP_Project2_PartC/best_tictac_model.pkl')
print("Model training and saving completed.")


# Evaluating the best model on test data
y_pred = best_model.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy: %.5f" % accuracy)  
precision = metrics.precision_score(y_test, y_pred,average='weighted')
print("Precision: %.5f" % precision)
recall = metrics.recall_score(y_test, y_pred,average='weighted')
print("Recall: %.5f" % recall)
f1 = metrics.f1_score(y_test, y_pred,average='weighted')
print("F1 Score: %.5f" % f1)


''' 
    Using the Kaggle function to compute ROC-AUC for multiclass classification 
    with slight modifications as referred during the lab week 10
'''
def roc_auc_score_multiclass(actual_class, pred_class, average = "weighted"):
    unique_class = set(actual_class)      
    roc_auc_dict = {}
    for per_class in unique_class:
        other_class = [x for x in unique_class if x != per_class]

        # Binary transformation (one-vs-rest)
        new_actual_class = [0 if x in other_class else 1 for x in actual_class]
        new_pred_class   = [0 if x in other_class else 1 for x in pred_class]

        # Compute binary ROC-AUC for this class
        roc_auc = roc_auc_score(new_actual_class, new_pred_class, average = average)
        roc_auc_dict[per_class] = roc_auc

    return roc_auc_dict

# Plot ROC/AUC curve (HistGradientBoostingClassifier)
y_true = y_test
y_pred = best_model.predict(X_test)

# Call your function
roc_dict = roc_auc_score_multiclass(y_true, y_pred)
print("Weighted-average AUC:", sum(roc_dict.values()) / len(roc_dict))