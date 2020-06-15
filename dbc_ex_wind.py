# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import datetime as dt
from io import StringIO

# Dash callbacks: https://dash.plot.ly/getting-started-part-2
# wind direction polar plot with dcc: https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-wind-streaming/app.py
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}
datafile = 'ex.dat'
dat_names = ['wdate','wind_dir','wind_speed','wind_gust','col5','humidity','col7','temp_out','col9','col10']
TESTDATA = StringIO("""
202003190115 359.000 0.000 0.000 100.000 97.000 55.500 27.700 24.986 9.120
202003190235 359.000 0.000 0.000 100.000 97.000 55.100 28.100 24.986 9.120
202003190350 359.000 0.000 0.000 100.000 97.000 54.800 28.500 24.986 9.120
202003190515 359.000 5.000 8.000 100.000 97.000 54.500 28.400 24.986 9.120
202003190635 359.000 0.000 0.000 100.000 97.000 54.000 28.000 24.986 9.120
202003190750 359.000 0.000 0.000 100.000 97.000 53.100 27.700 24.986 9.120
202003190915 359.000 0.000 0.000 100.000 97.000 53.300 29.000 24.986 9.120
202003191035 359.000 0.000 0.000 100.000 98.000 54.600 31.300 24.986 9.120
202003191150 241.000 0.000 0.000 100.000 98.000 56.100 32.600 24.986 9.120
202003191315 359.000 0.000 0.000 100.000 97.000 58.700 34.600 24.986 9.120
202003191435 359.000 0.000 0.000 100.000 97.000 59.700 33.500 24.986 9.120
202003191550 290.000 0.000 0.000 100.000 98.000 59.700 33.200 24.986 9.130
202003191715 15.000 0.000 0.000 100.000 98.000 59.600 32.600 24.986 9.160
202003191835 23.000 0.000 0.000 100.000 98.000 59.600 33.200 24.986 9.160
202003191950 23.000 0.000 0.000 100.000 98.000 59.100 32.800 24.986 9.160
202003192115 18.000 0.000 0.000 100.000 98.000 58.400 32.100 24.986 9.160
202003192235 22.000 0.000 0.000 100.000 98.000 57.700 32.500 24.986 9.160
202003192350 37.000 0.000 0.000 100.000 98.000 57.100 32.100 24.986 9.170
202003200115 41.000 0.000 0.000 100.000 98.000 56.700 31.600 24.986 9.170
202003200235 89.000 0.000 0.000 100.000 98.000 56.300 31.200 24.986 9.170
202003200350 93.000 0.000 0.000 100.000 98.000 55.700 30.100 24.986 9.170
202003200515 90.000 0.000 0.000 100.000 98.000 55.400 30.600 24.986 9.170
202003200635 359.000 0.000 0.000 100.000 98.000 54.800 29.400 24.986 9.170
202003200750 359.000 0.000 0.000 100.000 98.000 54.200 30.500 24.986 9.170
202003200915 60.000 0.000 0.000 100.000 98.000 55.200 31.600 24.986 9.170
202003201035 97.000 0.000 0.000 100.000 98.000 56.500 32.800 24.986 9.170
202003201150 359.000 3.000 6.000 100.000 98.000 58.800 34.600 24.986 9.170
202003201315 359.000 0.000 0.000 100.000 97.000 60.300 35.900 24.986 9.170
202003201435 359.000 0.000 0.000 100.000 97.000 61.300 36.900 24.986 9.170
202003201550 10.000 2.000 3.000 100.000 97.000 62.100 37.700 24.986 9.170
202003201715 16.000 0.000 0.000 100.000 97.000 62.400 37.100 24.986 9.170
202003201835 32.000 0.000 0.000 100.000 98.000 62.200 35.900 24.986 9.170
202003201950 97.000 1.000 4.000 100.000 98.000 61.400 33.300 24.986 9.190
202003202115 359.000 0.000 0.000 100.000 98.000 60.500 34.800 24.986 9.190
202003202235 105.000 0.000 5.000 100.000 98.000 59.700 34.800 24.986 9.190
202003202350 105.000 0.000 0.000 100.000 98.000 59.300 34.400 24.986 9.200
202003210115 102.000 0.000 0.000 100.000 98.000 58.800 33.400 24.986 9.220
202003210235 359.000 0.000 0.000 100.000 98.000 58.200 32.500 24.986 9.250
202003210350 359.000 0.000 6.000 100.000 98.000 57.700 32.800 24.986 9.260
202003210515 359.000 0.000 0.000 100.000 98.000 57.300 33.200 24.986 9.270
202003210635 359.000 0.000 0.000 100.000 98.000 57.000 32.800 24.986 9.280
202003210750 158.000 0.000 0.000 100.000 98.000 56.700 32.600 24.986 9.290
202003210915 158.000 0.000 0.000 100.000 98.000 56.700 32.000 24.986 9.320
202003211035 157.000 0.000 2.000 100.000 98.000 56.800 32.300 24.986 9.380
202003211150 162.000 0.000 6.000 100.000 98.000 57.100 34.200 24.986 9.410
202003211315 115.000 11.000 17.000 100.000 98.000 56.800 35.600 24.986 9.410
202003211435 137.000 2.000 6.000 100.000 98.000 57.400 36.000 24.986 9.410
202003211550 359.000 0.000 9.000 100.000 98.000 59.400 38.700 24.986 9.410
202003211715 359.000 0.000 0.000 100.000 98.000 61.100 38.000 24.986 9.410
202003211835 359.000 0.000 0.000 100.000 98.000 61.300 35.900 24.986 9.410
202003211950 359.000 0.000 4.000 100.000 98.000 60.700 36.200 24.986 9.410
202003212115 116.000 2.000 5.000 100.000 98.000 60.000 35.600 24.986 9.410
202003212235 359.000 7.000 10.000 100.000 98.000 59.400 36.000 24.986 9.410
202003212350 91.000 0.000 5.000 100.000 98.000 58.500 35.800 24.986 9.410
202003220115 359.000 10.000 11.000 100.000 98.000 58.100 35.900 24.986 9.410
202003220235 58.000 4.000 12.000 100.000 98.000 57.600 35.900 24.986 9.410
202003220350 67.000 1.000 7.000 100.000 98.000 57.300 36.700 24.986 9.410
202003220515 51.000 0.000 7.000 100.000 98.000 57.100 36.900 24.986 9.410
202003220635 66.000 0.000 8.000 100.000 98.000 56.800 35.900 24.986 9.410
202003220750 56.000 0.000 7.000 100.000 98.000 56.700 35.700 24.986 9.410
202003220915 66.000 0.000 9.000 100.000 99.000 56.400 35.800 24.986 9.420
202003221035 78.000 0.000 2.000 100.000 98.000 56.700 36.700 24.986 9.420
202003221150 359.000 0.000 7.000 100.000 98.000 56.800 37.400 24.986 9.440
202003221315 49.000 5.000 9.000 100.000 99.000 57.300 38.800 24.986 9.450
202003221435 359.000 0.000 3.000 100.000 98.000 58.100 39.700 24.986 9.450
202003221550 359.000 0.000 0.000 100.000 99.000 58.500 39.400 24.986 9.450
202003221705 359.000 0.000 0.000 100.000 99.000 59.000 39.800 24.986 9.460
""")
df = pd.read_csv(TESTDATA, sep=' ',names=dat_names,index_col=0,parse_dates=True)
df = df.drop_duplicates()
df.index = pd.to_datetime(df.index,format="%Y%m%d%H%M")
# the full index range
date_limits = [df.index.min(),df.index.max()]

N_DAYS = 20     # start with range slider of last N days
# use datetime, set earliest to 00:00 and latest to 23:59
datetime1 = dt.datetime(date_limits[1].year, date_limits[1].month, date_limits[1].day,hour=23,minute=59)
date1 = dt.date(date_limits[1].year, date_limits[1].month, date_limits[1].day)
datetime0 = dt.datetime(date_limits[0].year, date_limits[0].month, date_limits[0].day)
date0 = dt.date(date_limits[0].year, date_limits[0].month, date_limits[0].day)
date_range = date1 - date0  # integer number of days
# date0 no more than N_DAYS before date1
date0 = date0 if date_range <= dt.timedelta(days=N_DAYS) else date1 - dt.timedelta(days=N_DAYS)

df30 = df.loc[datetime0 : datetime1]

# TODO: I can select specific date like this: df.loc['2020-02-06'], even if the index contains HHMMSS.
# TODO: How to select a range of dates?

# generate a list of dates for the slider
def gen_date_list(date0,date1):
    d0 = dt.date(date0.year,date0.month,date0.day)
    d1 = dt.date(date1.year,date1.month,date1.day)
    ndate = (d1-d0).days + 1
    day_delta = dt.timedelta(days=1)
    dlist = [d0 + i*day_delta for i in range(ndate)]
    return dlist

day_list = gen_date_list(date0,date1)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,])

# Next dbc.Row contains two graphs side-by-side
row1 = dbc.Row(
    # style for Div that contains both wind speed and wind direction graphs
    # margin-bottom required for labels on date selector slider
    children=[
        # XY graph of wind speed, time on x-axis
        dbc.Col(width = 8, children=[
            dcc.Graph(
                id='wind-date-plot',
                style={'height': '80%'}
            ),
            html.Div(
                # date slider sits underneath the wind-speed plot
                dcc.Slider(
                    id='wind-date-slider',
                    included=False,
                    min=0,
                    max=len(day_list) - 1,
                    value=len(day_list) - 1,  # start at last day
                    marks={i: {'label': str(dm), 'style': {'transform': 'rotate(-40deg) translate(-40px,-20px)'}} for
                           i, dm in enumerate(day_list) if i % 2 == 0},
                    dots=True,
                ),
                # style for Div that contains Slider
                style={'width': "70%", "margin-left": "100px", }
            )
        ],className='h-100'
        ),
        # polar plot of wind speed and direction with hour slider
        dbc.Col(
            # style for Span that contains Graph and Slider
            #style=dict(display="inline-block", width="30%"),
            width = 4,
            children=[
                dcc.Graph(
                    id='wind-dir-plot',
                    style={'height': '80%'}
                ),
                html.Div(
                    # style for Div that contains Slider
                    style={'margin-top': '20px'},
                    children=[
                        dcc.Slider(
                            # style={'height':'inherit'},
                            id='hour-slider',
                            included=False,
                            min=0,
                            max=23,
                            value=0,  # start at zero hour
                            marks={str(hour): str(hour) for hour in range(0, 23, 2)},
                            step=None
                        ),
                    ],
                )],className='h-100'
        ),
    ], className='h-75'
)

# Second row of graphs
row2 = dbc.Row(children=[
        dbc.Col(width=6, children=[dcc.Graph(id='temp-out',className='h-100')],className='h-100'),
        dbc.Col(width=6, children=[dcc.Graph(id='rel-hum',className='h-100')],className='h-100'),
        ], className='h-25')
# must set fluid=True to occupy full width
app.layout = dbc.Container(children=[row1, row2], fluid=True, className='vh-100')

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
        'layout': dict(title={'text':'Wind Speed (every 5 minutes)','y':'0.8'}),
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

@app.callback(
    Output('temp-out', 'figure'),
    [Input('wind-date-slider', 'value')])
def update_temp_out_figure(selected_day):
    f_df = df30[str(date0+dt.timedelta(days=selected_day))]
    traces = []
    traces.append(dict(x=f_df.index,y=f_df['temp_out'],type='line',name=u'temperature'))
    return {
        'data': traces,
        'layout': dict(title={'text':'Temperature Outside','y':'0.5'}),
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
        'layout': dict(title={'text':'Relative Humidity','y':'1.0'},),
    }


if __name__ == '__main__':
    server = app.server
    app.run_server(debug=True, port=8050)
else:   # not __main__
    # when running by wsgi script
    app.config.update({
        'url_base_pathname':'/OOS-data/',
        'routes_pathname_prefix':'/OOS-data/',
        'requests_pathname_prefix':'/OOS-data/',
    })
    server = app.server
