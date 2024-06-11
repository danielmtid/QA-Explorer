import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import requests

app = dash.Dash(__name__)
app.title = 'QA Explorer'

engine = create_engine('mysql+pymysql://username:password@host:port/database')

def fetch_data():
    query = "SELECT * FROM test_results"
    df = pd.read_sql(query, engine)
    return df

def create_graphs():
    df = fetch_data()
    status_count = df['status'].value_counts().reset_index()
    status_count.columns = ['status', 'count']
    fig1 = px.bar(status_count, x='status', y='count', title='Resultados de Pruebas')
    fig2 = px.scatter(df, x='timestamp', y='duration', color='status', title='Duración de las Pruebas a lo Largo del Tiempo')
    return fig1, fig2

app.layout = html.Div(children=[
    html.H1(children='QA Explorer'),
    html.Div(children='Visualización y ejecución de resultados de pruebas en GitHub Actions.'),
    html.Button('Ejecutar Pruebas', id='run-tests-button', n_clicks=0),
    html.Div(id='test-output', children='Presiona el botón para ejecutar las pruebas.'),
    dcc.Graph(id='status-graph', figure=create_graphs()[0]),
    dcc.Graph(id='duration-graph', figure=create_graphs()[1]),
    dcc.Interval(id='interval-component', interval=1*60000, n_intervals=0)
])

@app.callback(
    [Output('status-graph', 'figure'), Output('duration-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    fig1, fig2 = create_graphs()
    return fig1, fig2

@app.callback(
    Output('test-output', 'children'),
    [Input('run-tests-button', 'n_clicks')]
)
def run_tests(n_clicks):
    if n_clicks > 0:
        response = requests.post('http://localhost:5000/run-tests')
        if response.status_code == 200:
            result = response.json()
            return html.Pre(result['output'])
        else:
            return html.Pre('Error al ejecutar las pruebas')
    return 'Presiona el botón para ejecutar las pruebas.'

if __name__ == '__main__':
    app.run_server(debug=True)
