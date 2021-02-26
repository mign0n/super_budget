import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output


def init_dashboard(server):
    dash_app = Dash(
        __name__,
        server=server,
        assets_folder='../static',
        assets_url_path='../static',
        routes_pathname_prefix='/diagram/',
        title='Understand your cash flow.'
    )

    dash_app.layout = html.Div(children=[
        html.H1(children='Dashboard is coming soon.'),
        html.Div(children=dcc.Graph(id='cash-flow'), className='card'),
        html.Div(children=dcc.Graph(id='cash-balance'), className='card'),
    ],
        className='wrapper')

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(app):
    @app.callback(
        [Output('cash-flow', 'figure'), Output('cash-balance', 'figure')],
        [
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'),
            Input('transaction-type-filter', 'value')
        ]
    )
    def update_graph(transaction_type, start_date, end_date):
        pass
