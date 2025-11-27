from dash import html, dcc

layout = html.Div(
    [
        html.H2("Matrix Operations Lab"),

        html.P("Enter matrices using comma-separated values per row, for example:"),
        html.Code("1,2,3\n4,5,6.5"),
        html.Br(),
        html.Br(),

        html.Div(
            [
                html.Div(
                    [
                        html.H4("Matrix A"),
                        dcc.Textarea(
                            id="mat-A",
                            placeholder="Enter Matrix A",
                            style={"width": "100%", "height": "120px"},
                        ),
                    ],
                    style={"flex": 1, "marginRight": "10px"},
                ),
                html.Div(
                    [
                        html.H4("Matrix B"),
                        dcc.Textarea(
                            id="mat-B",
                            placeholder="Enter Matrix B (if needed)",
                            style={"width": "100%", "height": "120px"},
                        ),
                    ],
                    style={"flex": 1},
                ),
            ],
            style={"display": "flex", "marginBottom": "15px"},
        ),

        html.Label("Operation"),
        dcc.Dropdown(
            id="mat-operation",
            options=[
                {"label": "A + B", "value": "add"},
                {"label": "A - B", "value": "sub"},
                {"label": "A × B", "value": "mul"},
                {"label": "Transpose A", "value": "tA"},
                {"label": "Transpose B", "value": "tB"},
                {"label": "Determinant |A|", "value": "detA"},
                {"label": "Determinant |B|", "value": "detB"},
            ],
            placeholder="Select operation",
            style={"width": "250px", "marginBottom": "10px"},
        ),

        html.Button("Compute", id="mat-run", n_clicks=0),

        html.Hr(),

        html.H3("Result"),
        html.Div(
            id="mat-result",
            style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"},
        ),
    ]
)
