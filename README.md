# Multi-Tab Data Science Web Application

A browser-based analytical platform developed using Plotly Dash. The
application integrates three core modules within a single interface:
Data Explorer, Regression Lab, and Matrix Lab. It is designed to support
data analysis, machine learning experimentation, and matrix computation
in an accessible and interactive manner.

## 1. Project Structure

    multi_tab_project/
    │
    ├── app.py                     # Main Dash application file
    ├── index.py                   # Base layout and navigation tabs
    │
    ├── pages/
    │   ├── data_explorer.py       # Data Explorer user interface
    │   ├── house_price.py         # Regression Lab user interface
    │   └── matrix_lab.py          # Matrix Lab user interface
    │
    ├── helpers/
    │   ├── eda_utils.py           # Functions for EDA operations
    │   ├── model_utils.py         # Model training and prediction utilities
    │   └── matrix_utils.py        # Matrix parsing and mathematical operations
    │
    ├── assets/
    │   └── style.css              # Custom styling for the application
    │
    ├── requirements.txt           # Python dependencies
    └── README.md                  # Project documentation

## 2. Project Overview

### 2.1 Data Explorer

The Data Explorer module allows users to upload CSV datasets and perform
basic exploratory analysis.

**Key capabilities:**

-   File upload and automatic parsing
-   Display of dataset dimensions and missing values
-   Summary statistics for numerical columns
-   Preview of the first ten rows
-   Correlation heatmap
-   2D histograms and scatter plots
-   3D scatter visualisation
-   Automatic support for integer, float, and decimal values

### 2.2 Regression Lab

The Regression Lab provides an environment for experimenting with
machine learning models.

**Features:**

-   CSV dataset upload
-   Selection of numerical feature columns
-   Selection of a target variable
-   Training of a Ridge Regression model with scaling
-   Display of evaluation metrics (MAE, RMSE, R²)
-   3D visualisation using any chosen numeric axes
-   Auto-generated input fields for prediction
-   Prediction results based on the trained model

### 2.3 Matrix Lab

The Matrix Lab enables interactive matrix computations with support for
integers, floats, and decimals.

**Supported operations:**

-   Matrix addition
-   Matrix subtraction
-   Matrix multiplication
-   Transpose
-   Determinant

## 3. Installation and Setup

### 3.1 Clone the Repository

``` bash
git clone https://github.com/your-username/multi_tab_project.git
cd multi_tab_project
```

### 3.2 Install Dependencies

Ensure Python 3.10+ is installed.

``` bash
pip install -r requirements.txt
```

### 3.3 Run the Application

``` bash
python app.py
```

Application will run at:

http://127.0.0.1:8050/

## 4. Technologies Used

-   Python
-   Plotly Dash
-   Dash Bootstrap Components
-   Pandas
-   NumPy
-   Scikit-learn
-   Gunicorn

## 5. Purpose of the Project

This project has been developed as part of academic coursework to
demonstrate:

-   Understanding of interactive web applications using Dash
-   Ability to perform exploratory data analysis
-   Practical knowledge of regression modelling
-   Implementation of mathematical computations
-   Skills in organising multi-page applications
