"""
Moduł definiujący układ interfejsu użytkownika aplikacji.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_layout(data_handler) -> dbc.Container:
    """Tworzy główny layout aplikacji.
    
    Args:
        data_handler: Obiekt dostarczający aktualne kursy walut
        
    Returns:
        dbc.Container: Gotowy kontener z całym UI
    """
    return dbc.Container([
        dcc.Store(id='store', data={'use_current': True}),
        html.H1("Kursy walut NBP", className="text-center my-3"),
        _create_converter_card(data_handler),
        _create_historical_card(),
    ], fluid=True, style={'padding': '15px', 'minHeight': '100vh'})


def _create_converter_card(data_handler) -> dbc.Card:
    """Tworzy kartę konwertera walut."""
    return dbc.Card([
        dbc.CardHeader("Wymiana walut"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Z waluty:"),
                    dcc.Dropdown(
                        id='from_currency',
                        options=sorted(
                            [{'label': k, 'value': k} for k in data_handler.current_rates.keys()],
                            key=lambda x: x['label']
                        ),
                        value='USD',
                        clearable=False
                    )
                ], md=5),
                dbc.Col([
                    dbc.Label("Na walutę:"),
                    dcc.Dropdown(
                        id='to_currency',
                        options=sorted(
                            [{'label': k, 'value': k} for k in data_handler.current_rates.keys()],
                            key=lambda x: x['label']
                        ),
                        value='PLN',
                        clearable=False
                    )
                ], md=5),
                dbc.Col([
                    dbc.Label("Ilość:"),
                    dcc.Input(
                        id='amount',
                        type='number',
                        value=1,
                        min=0,
                        className="form-control"
                    )
                ], md=2)
            ], className="g-2"),
            html.Div(id='output', className="mt-3"),
            dbc.Button(
                "Pokaż dzisiejszy kurs",
                id='reset_button',
                color="primary",
                className="mt-2",
                style={'display': 'none'}
            )
        ])
    ], className="mb-3 shadow")


def _create_historical_card() -> dbc.Card:
    """Tworzy kartę z wykresem historycznym."""
    return dbc.Card([
        dbc.CardHeader("Wykres zmiany kursu"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Okres:"),
                    dcc.Dropdown(
                        id='period_selector',
                        options=[
                            {'label': '1 miesiąc', 'value': 30},
                            {'label': '3 miesiące', 'value': 90},
                            {'label': '6 miesięcy', 'value': 180},
                            {'label': '1 rok', 'value': 365},
                            {'label': '5 lat', 'value': 1784},
                        ],
                        value=90,
                        clearable=False
                    )
                ], md=3),
                dbc.Col(dcc.Graph(id='history_graph'), md=9)
            ])
        ])
    ], className="shadow")