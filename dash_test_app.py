# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
#import cgi
#import cgitb
#cgitb.enable()

if False:
    server = flask.Flask(__name__)
    app = dash.Dash(__name__, server=server, url_base_pathname='/pyapps/')
else:
    #app = dash.Dash(__name__, url_base_pathname='/pyapps/')
    app = dash.Dash(__name__)
"""
app.config.update({
    #'url_base_pathname':'/pyapps/',
    'routes_pathname_prefix':'/pyapps/',
    'requests_pathname_prefix':'/pyapps/',
})
"""
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div(children=[
    html.H1('Hello Dash'),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
