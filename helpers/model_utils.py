import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_regression_model(df: pd.DataFrame, feature_cols, target_col):
    """
    Train a Ridge regression model using selected numeric feature columns
    and a numeric target column.

    Args:
        df           : input DataFrame
        feature_cols : list of feature column names
        target_col   : target column name

    Returns:
        model   : trained sklearn Pipeline
        metrics : dict with MAE, RMSE, R2
    """
    if df is None:
        raise ValueError("Dataframe is None.")

    if not feature_cols:
        raise ValueError("No feature columns selected.")

    if target_col is None:
        raise ValueError("Target column not selected.")

    # X and y
    X = df[feature_cols]
    y = df[target_col]

    # Basic check: all must be numeric
    if not all(pd.api.types.is_numeric_dtype(X[c]) for c in feature_cols):
        raise ValueError("All selected features must be numeric.")
    if not pd.api.types.is_numeric_dtype(y):
        raise ValueError("Target column must be numeric.")

    # Preprocess numeric features (scale)
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), feature_cols),
        ]
    )

    # Regression model
    model = Ridge(alpha=1.0)

    # Full pipeline
    pipe = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Fit model
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }

    return pipe, metrics
