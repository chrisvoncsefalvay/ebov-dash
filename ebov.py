# -*- coding: utf-8 -*-
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import plotly.graph_objs as gobs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']

external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts, server=server)
data = pd.read_csv(
    'https://data.humdata.org/dataset/0d089fa0-3567-4b01-9c03-39d340ff34e3/resource/c59b5722-ca4b-41ca-a446-472d6d824d01/download/ebola_data_db_format.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data[data['Date'] < datetime(2015, 12, 20, 0, 0, 0)]

# CONTROLLER
# ==========

country_selector = dcc.Dropdown(
    id='country-selector',
    options=[{'label': i, 'value': i} for i in data["Country"].unique()],
    value=["Guinea", "Liberia"],
    multi=True
)

indicator_selector = dcc.Dropdown(
    id='indicator-selector',
    options=[{'label': i, 'value': i} for i in data["Indicator"].unique()],
    value="Case fatality rate (CFR) of suspected Ebola cases",
    multi=False
)

# PLOT
# ====

plot = html.Div(id="plot-container",
                children=[dcc.Graph(id="main-plot")])

# STRUCTURE
# =========

header = html.Div([
    html.H1("The West African Ebolavirus Outbreak")
])

app.layout = html.Div([
    header,
    dcc.Loading(plot),
    country_selector,
    indicator_selector
])


# CHART UPDATING
# ==============

@app.callback(
    dash.dependencies.Output('main-plot', 'figure'),
    [
        dash.dependencies.Input('country-selector', 'value'),
        dash.dependencies.Input('indicator-selector', 'value')
    ]
)
def create_graph(country, indicator):
    df = data[data["Indicator"] == indicator]

    if isinstance(country, str):
        df = df[df["Country"] == country]
    else:
        df = df[df["Country"].isin(country)]

    traces = []
    for country in df["Country"].unique():
        _data = df[df["Country"] == country]
        traces.append(gobs.Scatter(
            x=_data['Date'],
            y=_data['value'],
            name=country
        ))

    return {
        'data': traces,
        'layout': gobs.Layout(
            xaxis={"title": "Date"},
            yaxis={"title": indicator},
            height=625,
            showlegend=True,
            hovermode="closest"
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
