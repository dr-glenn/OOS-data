import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(fluid=True,
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.P("This is column 1"),
                    width=8,
                    style={"height": "100%", "background-color": "red"},
                ),
                dbc.Col(
                    html.P("This is column 2"),
                    width=4,
                    style={"height": "100%", "background-color": "green"},
                ),
            ],
            className="h-75",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.P("This is column 3"),
                    width=8,
                    style={"height": "100%", "background-color": "blue"},
                ),
                dbc.Col(
                    html.P("This is column 4"),
                    width=4,
                    style={"height": "100%", "background-color": "cyan"},
                ),
            ],
            className="h-25",
        ),
    ],
    style={"height": "100vh"},
)

if __name__ == "__main__":
    app.run_server(debug=True)