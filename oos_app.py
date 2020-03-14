# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Dash callbacks: https://dash.plot.ly/getting-started-part-2

# wind direction polar plot with dcc: https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-wind-streaming/app.py

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

datafile = 'data/oosdata.2020'
dat_names = ['wdate','wind_dir','wind_speed','wind_gust','col5','humidity','col7','temp_out','col9','col10']
df = pd.read_csv(datafile, sep=' ',names=dat_names,index_col=0,parse_dates=True)
df = df.drop_duplicates()
#df.describe()
df.index = pd.to_datetime(df.index,format="%Y%m%d%H%M")

# get Dataframe index numbers for first record of each day
def get_day_indices(df):
    '''
    :return: days: list of tuple(str(YYYY-mm-DD),loc in df.index)
    '''
    days = []
    dt_keys = {}
    for dt0 in df.index:
        dt_key = str(dt0.year) + "-" + str(dt0.month) + "-" + str(dt0.day)
        if not dt_key in dt_keys:
            # Store first index that matches yr-mon-day, skip all others
            dt_keys[dt_key] = df.index.get_loc(dt0)
            days.append((dt_key,dt_keys[dt_key]))
    return days

day_marks = get_day_indices(df)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='OOS Weather'),

    html.Div(children='''
        Built with Dash, a web app framework for Python
    '''),

    dcc.Graph(
        id='wind-date-plot',
        figure={
            'layout': {
                'title': 'Winds from Oliver Observing Station'
            }
        }
    ),
    
    html.Div(
        dcc.Slider(
            id='wind-date-slider',
            min = 0,
            max = len(day_marks)-2,    # -2 because we cannot select last date as start point
            value = 0,
            marks={i: 'Day {}'.format(i) if i == 0 else str(i) for i in range(len(day_marks))},
            
        ),style={"width":"80%","margin":"auto"}
    ),
])


@app.callback(
    Output('wind-date-plot', 'figure'),
    [Input('wind-date-slider', 'value')])
def update_figure(selected_day):
    f_df = df[day_marks[selected_day][1]:day_marks[selected_day+1][1]]
    traces = []
    traces.append(dict(x=f_df.index,y=f_df['wind_speed'],type='line',name=u'wind_speed'))
    traces.append(dict(x=f_df.index,y=f_df['wind_gust'],type='line',name=u'wind_gust'))

    return {
        'data': traces,
        'layout': dict(title='Wind Speed'),
    }


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)