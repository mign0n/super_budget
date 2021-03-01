import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output
from datetime import date, timedelta
from flask_login import current_user
from webapp.main.models import Category, Transaction

TODAY = date.today()
MONTH_AGO = TODAY - timedelta(days=30)


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
        html.H1(children='Dashboard is coming soon.', className='header-title'),
        html.Div(children=[
            html.Div(children=[
                html.Div(children='Transaction type'),
                dcc.Dropdown(
                    id='transaction-type-filter',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'Expenses', 'value': False},
                        {'label': 'Incomes', 'value': True},
                    ],
                    value='all',
                    clearable=False,
                    className='dropdown'
                )
            ]),
            html.Div(children=[
                html.Div(children='Date Range'),
                dcc.DatePickerRange(
                    id='date-range',
                    # min_date_allowed='2000-01-01',
                    max_date_allowed=TODAY,
                    start_date=MONTH_AGO,
                    end_date=TODAY,
                    display_format='DD.MM.YYYY'
                )
            ]),
        ],
            className='menu'
        ),
        html.Div(children=[
            html.Div(children=dcc.Graph(
                id='cash-flow',
            ), className='card'),
            html.Div(children=dcc.Graph(
                id='cash-balance',
            ), className='card'),
        ],
            className='wrapper')

    ])

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(app):
    @app.callback(
        [Output('cash-flow', 'figure'), Output('cash-balance', 'figure')],
        [
            Input('transaction-type-filter', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'),
        ]
    )
    def update_graph(transaction_type, start_date, end_date):
        dates, values = get_transactions_data(transaction_type, start_date, end_date)
        cash_flow_figure = {
            'data': [{'x': dates, 'y': values, 'type': 'bar'}],
            'layout': {
                'title': {
                    'text': 'Cash flow'
                }
            }
        }
        cash_balance_figure = {
            'data': [
                # mock object
                {'x': dates, 'y': [100000 - 1100, 93300, 91800, 88470], 'type': 'line', 'name': 'Balance'},
            ],
            'layout': {
                'title': {
                    'text': 'Balance'
                }
            }
        }
        return cash_flow_figure, cash_balance_figure


def get_transactions_data(trans_type, start_date, end_date):
    mask = [
        (Transaction.user_id == current_user.id),
        (Transaction.date >= start_date),
        (Transaction.date <= end_date)
    ]
    if isinstance(trans_type, bool):
        mask.append(
            (Transaction.trans_cat.has(Category.is_income == trans_type))
        )

    filtered_transactions = Transaction.query.filter(
        *mask
    ).order_by(Transaction.date.asc())
    transaction_dates = [transaction.date for transaction in filtered_transactions]
    transaction_values = [transaction.value for transaction in filtered_transactions]

    return transaction_dates, transaction_values
