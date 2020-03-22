# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import datetime as dt

# Dash callbacks: https://dash.plot.ly/getting-started-part-2

# wind direction polar plot with dcc: https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-wind-streaming/app.py

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

datafile = 'data/oosdata.2020'
dat_names = ['wdate','wind_dir','wind_speed','wind_gust','col5','humidity','col7','temp_out','col9','col10']
# TODO: can I read just a select date range?
df = pd.read_csv(datafile, sep=' ',names=dat_names,index_col=0,parse_dates=True)
df = df.drop_duplicates()
#df.describe()
df.index = pd.to_datetime(df.index,format="%Y%m%d%H%M")
# the full index range
date_limits = [df.index.min(),df.index.max()]
# start with range slider of last N days
N_DAYS = 20
date1 = dt.date(date_limits[1].year, date_limits[1].month, date_limits[1].day)
date0 = dt.date(date_limits[0].year, date_limits[0].month, date_limits[0].day)
date_range = date1 - date0
date0 = date0 if date_range <= dt.timedelta(days=N_DAYS) else date1 - dt.timedelta(days=N_DAYS)

df30 = df.loc[date0 : date1]

# TODO: I can select specific date like this: df.loc['2020-02-06'], even if the index contains HHMMSS.
# TODO: How to select a range of dates?

# TODO: make a range slider that defaults to one day selection of most recent 24 hours
# TODO: make a range slider to select hours, esp. for wind_dir polar plot

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

# generate a list of dates for the slider
def gen_date_list(date0,date1):
    d0 = dt.date(date0.year,date0.month,date0.day)
    d1 = dt.date(date1.year,date1.month,date1.day)
    ndate = (d1-d0).days
    day_delta = dt.timedelta(days=1)
    dlist = [d0 + i*day_delta for i in range(ndate)]
    return dlist

day_list = gen_date_list(date0,date1)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='OOS Weather'),

    html.Div(children='''
        Built with Dash, a web app framework for Python
    '''),
    # Next Div contains two graphs side-by-side, using display="inline-block"
    html.Div(children=[
        # XY graph of wind speed, time on x-axis
        html.Span([
            dcc.Graph(
                id='wind-date-plot',
            ),
            html.Div(
                # date slider sits underneath the wind-speed plot
                dcc.Slider(
                    id='wind-date-slider',
                    min = 0,
                    max = len(day_list)-2,    # -2 because we cannot select last date as start point
                    value = 0,
                    #marks={i: {'label':str(dm),'style':{'transform':'rotate(40deg) translate(0px,20px)'}} for i,dm in enumerate(day_list) if i%2 == 0},
                    marks={i: {'label':str(dm),'style':{'transform':'rotate(-40deg) translate(-40px,-20px)'}} for i,dm in enumerate(day_list) if i%2 == 0},
                    dots=True,
                    # transform: rotate(20deg)
                ),
                style={'width':"70%","margin-left":"100px",}
            )],
            style={"display":"inline-block","width":"60%"},
        ),
        # polar plot of wind speed and direction
        html.Span([
            dcc.Graph(
                id='wind-dir-plot',
            ),
            html.Div(
                dcc.Slider(
                    id='hour-slider',
                    min=0,
                    max=23,
                    value=0,
                    marks={str(hour): str(hour) for hour in range(0,23,2)},
                    step=None
                ),
                style={'margin-top':'20px'},
            )],
            style=dict(display="inline-block",width="20%")
        ),
        ],
        style={"margin-bottom":"60px",}
    ),
    
    # Second row of graphs
    html.Div(children=[
        html.Span(
            dcc.Graph(
                id='temp-out',
            ),
            style={'display':'inline-block'},
        ),
        html.Span(
            dcc.Graph(
                id='rel-hum',
            ),
            style={'display':'inline-block'},
        ),
        ]
    ),
])


@app.callback(
    Output('wind-date-plot', 'figure'),
    [Input('wind-date-slider', 'value')])
def update_wind_speed_figure(selected_day):
    f_df = df30[str(date0+dt.timedelta(days=selected_day))]
    traces = []
    traces.append(dict(x=f_df.index,y=f_df['wind_speed'],type='line',name=u'wind_speed'))
    traces.append(dict(x=f_df.index,y=f_df['wind_gust'],type='line',name=u'wind_gust'))

    return {
        'data': traces,
        'layout': dict(title='Wind Speed (every 5 minutes)'),
    }

@app.callback(
    Output('temp-out', 'figure'),
    [Input('wind-date-slider', 'value')])
def update_temp_out_figure(selected_day):
    f_df = df30[str(date0+dt.timedelta(days=selected_day))]
    traces = []
    traces.append(dict(x=f_df.index,y=f_df['temp_out'],type='line',name=u'temperature'))
    return {
        'data': traces,
        'layout': dict(title='Temperature Outside', height=400),
    }

@app.callback(
    Output('rel-hum', 'figure'),
    [Input('wind-date-slider', 'value')])
def update_rel_hum_figure(selected_day):
    f_df = df30[str(date0+dt.timedelta(days=selected_day))]
    traces = []
    traces.append(dict(x=f_df.index,y=f_df['humidity'],type='line',name=u'humidity'))

    return {
        'data': traces,
        'layout': dict(title='Relative Humidity', height=400),
    }


@app.callback(
    Output('wind-dir-plot', 'figure'),
    [Input('wind-date-slider', 'value'),
     Input('hour-slider','value')])
def update_wind_dir_figure(selected_day, selected_hour):
    f_df = df30[str(date0+dt.timedelta(days=selected_day))]
    # Max wind speed in this time
    wmax = f_df['wind_speed'].max()
    wmax = int(round(wmax,-1))
    tick_int = 10 if wmax >= 20 else 5
    # Get 4 hour slice for this graph
    d0 = f_df.index[0]   # it's a datetime
    hour0 = dt.timedelta(hours=selected_hour)
    h1 = selected_hour+4 if selected_hour <= 20 else 24
    hour1 = dt.timedelta(hours=h1)
    f_df = f_df.loc[str(d0+hour0) : str(d0+hour1)]
    # Wind direction of 359 is almost certainly bogus, so remove
    winds = f_df.loc[df['wind_dir'] != 359.0][['wind_dir','wind_speed']]
    val = winds["wind_speed"]
    direction = winds["wind_dir"]

    data = [
        dict(
            type="scatterpolar",
            r=val,
            theta=direction,
            mode="markers",
            marker=dict(color='yellow'),
        )
    ]

    layout = dict(
        height=350,
        #plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        autosize=False,
        polar=dict(
            bgcolor=app_color["graph_line"],
            radialaxis=dict(range=[0, wmax], angle=0, dtick=tick_int),
            angularaxis=dict(showline=False, tickcolor="white",rotation=90,direction='clockwise'),
        ),
        showlegend=False,
        title='Wind Direction (4 hours)',
    )

    return {
        'data': data,
        'layout': layout,
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)