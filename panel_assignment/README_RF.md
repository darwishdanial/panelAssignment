# README.md

# Panel Assignment ML Pipeline - Overview

This repository contains a machine learning pipeline for predicting academic panel assignments based on project type and area. The workflow is organized in the `panel_assignment/notebooks_RF` folder, with each notebook representing a key step in the process.

## Workflow Overview

## 0. Data Download (`download_data.py`, `merge_RF_data.py`)

- Downloads raw project and examiner data from UTM web API endpoints.
- Uses `src/data/loader.py` to fetch JSON and save as Excel files:
  - `data/raw/project_data.xlsx`
  - `data/raw/examiner_data.xlsx`
- Uses `src/data/mergerRF.py` to merge project_data and examiner_data to 3 columns:
  - `project_type` 
  - `project_area` 
  - `lecturer_name` 
- This step should be run **before** starting the notebook pipeline to ensure all required raw data is available.

### 1. Data Processing (`1dataProcessing.ipynb`)
- Loads merged data.
- Encodes categorical variables:
  - `project_type` → `type_encoded`
  - `project_area` → `area_encoded`
  - `lecturer_name` → `lecturer_encoded`
- Explores class imbalance and augments rare classes for better model training.
- Saves processed datasets for downstream tasks.

### 2. File Comparison (`2compareFile.ipynb`)
- Compares processed Excel files to ensure consistency between ML and Web app outputs.

### 3. Model Comparison (`3compareModel.ipynb`)
- Trains and evaluates multiple classifiers:
  - Decision Tree
  - Random Forest
  - Logistic Regression
  - k-NN
  - Naive Bayes
- Uses both standard accuracy and a custom historical validation metric.

### 4. Class Balance Comparison (`4compareBalance.ipynb`)
- Compares model performance with and without class balancing (`class_weight='balanced'`).
- Evaluates using custom and standard metrics for Decision Tree and Random Forest.

### 5. Decision Tree Hyperparameter Tuning (`5hypDecisionTree.ipynb`)
- Performs grid search over Decision Tree hyperparameters:
  - `max_depth`
  - `min_samples_split`
  - `criterion`
  - `random_state`
- Identifies the best parameter combination for optimal accuracy.

### 6. Random Forest Hyperparameter Tuning (`6hypRainforest.ipynb`)
- Performs grid search over Random Forest hyperparameters:
  - `n_estimators`
  - `random_state`
  - `max_leaf_nodes`
  - `max_depth`
- Finds the best configuration for model performance.

### 7. Final Model Training & Export (`7finalModel.ipynb`)
- Trains the final Random Forest model using the best parameters.
- Saves the trained model as `panel_model.joblib` in the `model` directory for API deployment.

## Outputs

- Processed datasets in `data/processed/`
- Encoded mapping files for panels and areas
- Trained model in `model/panel_model.joblib`

## Usage

1. Run notebooks in order for full pipeline execution.
2. Use the exported model in the FastAPI service for real-time predictions.

---

For details on each step, see the corresponding notebook in `panel_assignment/notebooks_RF