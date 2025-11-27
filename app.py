from dash import Dash, dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import dash_table

import pages.data_explorer as de
import pages.house_price as hp
import pages.matrix_lab as ml
from index import layout as main_layout
from helpers.eda_utils import parse_contents, basic_info, split_columns
from helpers.model_utils import train_regression_model
from helpers.matrix_utils import (
    parse_matrix,
    matrix_add,
    matrix_sub,
    matrix_mul,
    matrix_transpose,
    matrix_det,
)



# ============== GLOBALS FOR REGRESSION MODEL ==============

hp_model = None          # trained sklearn Pipeline
hp_feature_cols = None   # list of feature column names
hp_target_col = None     # target column name


# ============== APP SETUP ==============

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

# Main layout with tabs
app.layout = main_layout


# ============== TAB SWITCHING ==============

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
)
def render_tab_content(tab_value):
    if tab_value == "tab-eda":
        return de.layout
    elif tab_value == "tab-house":
        return hp.layout
    elif tab_value == "tab-matrix":
        return ml.layout
    # default
    return de.layout


# ============== EDA CALLBACKS (DATA EXPLORER) ==============

@app.callback(
    Output("eda-data-store", "data"),
    Output("eda-file-info", "children"),
    Output("eda-preview-table", "children"),
    Output("eda-summary", "children"),
    Input("eda-upload", "contents"),
    State("eda-upload", "filename"),
    prevent_initial_call=True,
)
def handle_upload(contents, filename):
    """Handle CSV upload, show info, preview, and summary, store df as JSON."""
    if contents is None:
        return None, "", "", ""

    try:
        df = parse_contents(contents, filename)
    except Exception as e:
        return None, f"Error reading file: {e}", "", ""

    info = basic_info(df)
    file_info = (
        f"Loaded file: {filename} | "
        f"Rows: {info['rows']} | Columns: {info['cols']} | "
        f"Missing values: {info['missing']}"
    )

    # preview table
    preview = dash_table.DataTable(
        data=df.head(10).to_dict("records"),
        columns=[{"name": c, "id": c} for c in df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
    )

    # summary for numeric columns
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        desc = numeric_df.describe().T.round(3)
        summary_table = dash_table.DataTable(
            data=desc.reset_index().to_dict("records"),
            columns=[{"name": c, "id": c} for c in desc.reset_index().columns],
            style_table={"overflowX": "auto"},
        )
    else:
        summary_table = "No numeric columns found."

    # store full dataframe as JSON
    return df.to_json(date_format="iso", orient="split"), file_info, preview, summary_table


@app.callback(
    Output("eda-corr-heatmap", "figure"),
    Output("eda-x-col", "options"),
    Output("eda-y-col", "options"),
    Output("eda-x3", "options"),
    Output("eda-y3", "options"),
    Output("eda-z3", "options"),
    Input("eda-data-store", "data"),
)
def update_corr_and_dropdowns(json_data):
    """Update correlation heatmap and dropdown options when data changes."""
    if json_data is None:
        return {}, [], [], [], [], []

    df = pd.read_json(json_data, orient="split")
    numeric_cols, _ = split_columns(df)

    # correlation heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Viridis",
            aspect="auto",
            title="Correlation matrix",
        )
    else:
        fig = {}

    options = [{"label": c, "value": c} for c in numeric_cols]

    return fig, options, options, options, options, options


@app.callback(
    Output("eda-2d-plot", "figure"),
    Input("eda-data-store", "data"),
    Input("eda-plot-type", "value"),
    Input("eda-x-col", "value"),
    Input("eda-y-col", "value"),
)
def update_2d_plot(json_data, plot_type, x_col, y_col):
    """Update 2D histogram or scatter plot."""
    if json_data is None or x_col is None:
        return {}

    df = pd.read_json(json_data, orient="split")

    if plot_type == "hist":
        fig = px.histogram(df, x=x_col, nbins=30, title=f"Histogram of {x_col}")
    else:
        if y_col is None:
            return {}
        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")

    return fig


@app.callback(
    Output("eda-3d-scatter", "figure"),
    Input("eda-data-store", "data"),
    Input("eda-x3", "value"),
    Input("eda-y3", "value"),
    Input("eda-z3", "value"),
)
def update_3d_scatter(json_data, x, y, z):
    """Update 3D scatter plot."""
    if json_data is None or x is None or y is None or z is None:
        return {}

    df = pd.read_json(json_data, orient="split")

    fig = px.scatter_3d(
        df,
        x=x,
        y=y,
        z=z,
        title=f"3D scatter: {x}, {y}, {z}",
    )
    return fig


# ============== REGRESSION LAB CALLBACKS (UPLOAD-BASED) ==============

# 1) Handle upload for House Price / Regression Lab
@app.callback(
    Output("hp-data-store", "data"),
    Output("hp-file-info", "children"),
    Output("hp-feature-cols", "options"),
    Output("hp-target-col", "options"),
    Output("hp-x3", "options"),
    Output("hp-y3", "options"),
    Output("hp-z3", "options"),
    Input("hp-upload", "contents"),
    State("hp-upload", "filename"),
)
def hp_handle_upload(contents, filename):
    if contents is None:
        return None, "", [], [], [], [], []

    try:
        df = parse_contents(contents, filename)
    except Exception as e:
        return None, f"Error reading file: {e}", [], [], [], [], []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    opts = [{"label": c, "value": c} for c in numeric_cols]

    info = f"Loaded file: {filename} | Rows: {df.shape[0]} | Cols: {df.shape[1]}"

    return df.to_json(orient="split"), info, opts, opts, opts, opts, opts


# 2) Train model on selected features / target
@app.callback(
    Output("hp-metrics", "children"),
    Output("hp-3d-plot", "figure"),
    Input("hp-train-btn", "n_clicks"),
    State("hp-data-store", "data"),
    State("hp-feature-cols", "value"),
    State("hp-target-col", "value"),
    State("hp-x3", "value"),
    State("hp-y3", "value"),
    State("hp-z3", "value"),
    prevent_initial_call=True,
)
def hp_train_model(n_clicks, json_df, feature_cols, target_col, x3, y3, z3):
    global hp_model, hp_feature_cols, hp_target_col

    if json_df is None:
        return "Upload a dataset first.", {}

    if not feature_cols or target_col is None:
        return "Select feature column(s) and target column.", {}

    df = pd.read_json(json_df, orient="split")

    # train model using helper
    hp_model, metrics = train_regression_model(df, feature_cols, target_col)
    hp_feature_cols = feature_cols
    hp_target_col = target_col

    metrics_div = html.Div(
        [
            html.P(f"MAE:  {metrics['MAE']:.3f}"),
            html.P(f"RMSE: {metrics['RMSE']:.3f}"),
            html.P(f"R²:   {metrics['R2']:.3f}"),
        ]
    )

    # 3D visualization
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    fig = {}

    # If user selected x3,y3,z3 use them; else try first 3 numeric cols
    if x3 and y3 and z3:
        try:
            fig = px.scatter_3d(df, x=x3, y=y3, z=z3, color=target_col,
                                title=f"3D scatter: {x3}, {y3}, {z3}")
        except Exception:
            fig = {}
    elif len(numeric_cols) >= 3:
        x3, y3, z3 = numeric_cols[:3]
        fig = px.scatter_3d(df, x=x3, y=y3, z=z3, color=target_col,
                            title=f"3D scatter: {x3}, {y3}, {z3}")

    return metrics_div, fig


# 3) Create dynamic input fields for prediction based on selected features
@app.callback(
    Output("hp-predict-inputs", "children"),
    Input("hp-feature-cols", "value"),
)
def hp_make_predict_inputs(cols):
    if not cols:
        return "Select feature columns first."

    inputs = []
    for c in cols:
        inputs.append(
            html.Div(
                [
                    html.Label(c),
                    dcc.Input(
                        id={"type": "hp-input", "index": c},
                        type="number",
                        step=0.1,
                        style={"width": "100%"},
                    ),
                ],
                style={"marginBottom": "10px"},
            )
        )

    return inputs


# 4) Predict using the trained model and dynamic feature inputs
@app.callback(
    Output("hp-predict-output", "children"),
    Input("hp-predict-btn", "n_clicks"),
    State("hp-data-store", "data"),
    State("hp-feature-cols", "value"),
    State("hp-target-col", "value"),
    State({"type": "hp-input", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def hp_predict(n_clicks, json_df, feature_cols, target_col, values):
    global hp_model

    if hp_model is None:
        return "Train a model first."

    if json_df is None:
        return "Upload a dataset first."

    if not feature_cols:
        return "Select feature columns."

    if values is None or len(values) != len(feature_cols):
        return "Enter values for all feature inputs."

    # Check for missing values
    for col, val in zip(feature_cols, values):
        if val is None:
            return f"Enter a value for feature '{col}'."

    # Build one-row DataFrame for prediction
    data = {col: [float(val)] for col, val in zip(feature_cols, values)}
    row = pd.DataFrame(data)

    try:
        pred = hp_model.predict(row)[0]
    except Exception as e:
        return f"Prediction error: {e}"

    return f"Predicted {target_col}: {pred:.4f}"

# ============== MATRIX LAB CALLBACKS ==============

@app.callback(
    Output("mat-result", "children"),
    Input("mat-run", "n_clicks"),
    State("mat-A", "value"),
    State("mat-B", "value"),
    State("mat-operation", "value"),
    prevent_initial_call=True,
)
def mat_compute(n_clicks, A_text, B_text, op):
    if op is None:
        return "Select an operation."

    # Parse A
    try:
        A = parse_matrix(A_text)
    except Exception as e:
        return f"A error: {e}"

    # Parse B only if needed
    B = None
    if op in ("add", "sub", "mul", "tB", "detB"):
        try:
            B = parse_matrix(B_text)
        except Exception as e:
            return f"B error: {e}"

    try:
        if op == "add":
            result = matrix_add(A, B)
        elif op == "sub":
            result = matrix_sub(A, B)
        elif op == "mul":
            result = matrix_mul(A, B)
        elif op == "tA":
            result = matrix_transpose(A)
        elif op == "tB":
            result = matrix_transpose(B)
        elif op == "detA":
            result = matrix_det(A)
        elif op == "detB":
            result = matrix_det(B)
        else:
            return "Unknown operation."

        return str(result)

    except Exception as e:
        return f"Error: {e}"

# ============== MAIN ==============

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)

