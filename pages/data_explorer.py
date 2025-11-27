from dash import html, dcc

layout = html.Div(
    [
        html.H2("Data Explorer"),

        # Upload component
        dcc.Upload(
            id="eda-upload",
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

        # Store to keep the dataframe JSON in memory
        dcc.Store(id="eda-data-store"),

        # File info text
        html.Div(id="eda-file-info", style={"marginBottom": "15px"}),

        html.H3("Preview"),
        html.Div(id="eda-preview-table"),

        html.Hr(),

        html.H3("Summary (numeric columns)"),
        html.Div(id="eda-summary"),

        html.Hr(),

        html.H3("Correlation Heatmap"),
        dcc.Graph(id="eda-corr-heatmap"),

        html.Hr(),

        html.H3("2D Plot"),
        html.Div(
            [
                html.Label("Plot Type"),
                dcc.Dropdown(
                    id="eda-plot-type",
                    options=[
                        {"label": "Histogram", "value": "hist"},
                        {"label": "Scatter", "value": "scatter"},
                    ],
                    value="hist",
                    style={"width": "200px"},
                ),
            ],
            style={"marginBottom": "10px"},
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Label("X axis"),
                        dcc.Dropdown(id="eda-x-col"),
                    ],
                    style={"flex": 1, "marginRight": "10px"},
                ),
                html.Div(
                    [
                        html.Label("Y axis (for scatter)"),
                        dcc.Dropdown(id="eda-y-col"),
                    ],
                    style={"flex": 1},
                ),
            ],
            style={"display": "flex", "marginBottom": "10px"},
        ),

        dcc.Graph(id="eda-2d-plot"),

        html.Hr(),

        html.H3("3D Scatter"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("X axis"),
                        dcc.Dropdown(id="eda-x3"),
                    ],
                    style={"flex": 1, "marginRight": "10px"},
                ),
                html.Div(
                    [
                        html.Label("Y axis"),
                        dcc.Dropdown(id="eda-y3"),
                    ],
                    style={"flex": 1, "marginRight": "10px"},
                ),
                html.Div(
                    [
                        html.Label("Z axis"),
                        dcc.Dropdown(id="eda-z3"),
                    ],
                    style={"flex": 1},
                ),
            ],
            style={"display": "flex", "marginBottom": "10px"},
        ),

        dcc.Graph(id="eda-3d-scatter"),
    ]
)
