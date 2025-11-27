from dash import html, dcc

layout = html.Div(
    [
        html.H2("Regression Lab"),

        html.P(
            "Upload any CSV with numeric columns, select feature columns and "
            "a numeric target column, train a Ridge regression model, "
            "visualize in 3D, and run predictions."
        ),

        # Upload CSV
        dcc.Upload(
            id="hp-upload",
            children=html.Div(["Drag and drop or ", html.A("select a CSV file")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "marginBottom": "15px",
            },
            multiple=False,
        ),

        # Store for dataset
        dcc.Store(id="hp-data-store"),

        # File info
        html.Div(id="hp-file-info", style={"marginBottom": "10px"}),

        html.H4("Feature and target selection"),
        html.Div(
            [
                dcc.Dropdown(
                    id="hp-feature-cols",
                    multi=True,
                    placeholder="Select numeric feature columns",
                    style={"marginBottom": "10px"},
                ),
                dcc.Dropdown(
                    id="hp-target-col",
                    placeholder="Select numeric target column",
                    style={"marginBottom": "10px"},
                ),
            ]
        ),

        html.Button("Train model", id="hp-train-btn", n_clicks=0),

        html.Hr(),

        html.H3("Model performance"),
        html.Div(id="hp-metrics"),

        html.H3("3D visualization"),
        html.Div(
            [
                dcc.Dropdown(
                    id="hp-x3",
                    placeholder="X axis (numeric column)",
                    style={"marginBottom": "5px"},
                ),
                dcc.Dropdown(
                    id="hp-y3",
                    placeholder="Y axis (numeric column)",
                    style={"marginBottom": "5px"},
                ),
                dcc.Dropdown(
                    id="hp-z3",
                    placeholder="Z axis (numeric column)",
                    style={"marginBottom": "10px"},
                ),
            ],
            style={"maxWidth": "400px"},
        ),
        dcc.Graph(id="hp-3d-plot"),

        html.Hr(),

        html.H3("Predict"),
        html.Div(
            id="hp-predict-inputs",
            style={"maxWidth": "400px"},
        ),
        html.Button(
            "Predict", id="hp-predict-btn", n_clicks=0, style={"marginTop": "10px"}
        ),
        html.Div(
            id="hp-predict-output",
            style={"marginTop": "10px", "fontWeight": "bold"},
        ),
    ]
)
