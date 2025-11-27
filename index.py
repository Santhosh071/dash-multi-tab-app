from dash import dcc, html

layout = html.Div(
    [
        html.H1("Multi-Tab Data Science App", style={"textAlign": "center"}),

        dcc.Tabs(
            id="tabs",
            value="tab-eda",
            children=[
                dcc.Tab(label="Data Explorer", value="tab-eda"),
                dcc.Tab(label="Regression Lab", value="tab-house"),
                dcc.Tab(label="Matrix Lab", value="tab-matrix"),
            ],
        ),

        html.Div(id="tab-content", style={"marginTop": "20px"}),
    ]
)
