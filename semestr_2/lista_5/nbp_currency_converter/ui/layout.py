"""
Module defining the user interface layout for the application.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from typing import Dict, List, Any, Optional

from config import config
from data.handler import NBPDataHandler


def create_layout(data_handler: NBPDataHandler) -> dbc.Container:
    """Create the main application layout.
    
    Args:
        data_handler: Object providing currency rate data
        
    Returns:
        dbc.Container: Container with the complete UI
    """
    return dbc.Container([
        # Application state store
        dcc.Store(id='app-state', data={'use_current': True}),
        
        # Header
        _create_header(),
        
        # Currency converter card
        _create_converter_card(data_handler),
        
        # Historical data card
        _create_historical_card(),
        
        # Footer
        _create_footer()
    ], fluid=True, className="p-4 min-vh-100")


def _create_header() -> html.Div:
    """Create the application header.
    
    Returns:
        html.Div: Header component
    """
    app_title = config.get("app", "title", "NBP Currency Converter")
    
    return html.Div([
        html.H1(app_title, className="text-center mb-4 mt-3"),
        html.P(
            "Real-time currency conversion and historical exchange rate using data from the National Bank of Poland.",
            className="text-center text-muted mb-4"
        )
    ])


def _create_converter_card(data_handler: NBPDataHandler) -> dbc.Card:
    """Create the currency converter card.
    
    Args:
        data_handler: Object providing currency rate data
        
    Returns:
        dbc.Card: Currency converter card component
    """
    # Get currency options
    currency_options = _get_currency_options(data_handler)
    
    # Get default values from config
    default_amount = config.get("ui", "default_amount", 1)
    default_from = config.get("ui", "default_from_currency", "USD")
    default_to = config.get("ui", "default_to_currency", "PLN")
    
    return dbc.Card([
        dbc.CardHeader([
            html.H4("Currency Converter", className="mb-0"),
        ]),
        dbc.CardBody([
            dbc.Row([
                # Source currency
                dbc.Col([
                    dbc.Label("From Currency:", html_for="from-currency-dropdown"),
                    dcc.Dropdown(
                        id='from-currency-dropdown',
                        options=currency_options,
                        value=default_from,
                        clearable=False,
                        className="mb-3"
                    )
                ], md=5),
                
                # Target currency
                dbc.Col([
                    dbc.Label("To Currency:", html_for="to-currency-dropdown"),
                    dcc.Dropdown(
                        id='to-currency-dropdown',
                        options=currency_options,
                        value=default_to,
                        clearable=False,
                        className="mb-3"
                    )
                ], md=5),
                
                # Amount input
                dbc.Col([
                    dbc.Label("Amount:", html_for="amount-input"),
                    dbc.Input(
                        id='amount-input',
                        type='number',
                        value=default_amount,
                        min=0.01,
                        step=0.01,
                        className="mb-3"
                    )
                ], md=2)
            ]),
            
            # Conversion result
            html.Div(id='conversion-result', className="my-3"),
            
            # Swap currencies button
            dbc.Button(
                [html.I(className="bi bi-arrow-left-right me-2"), "Swap Currencies"],
                id='swap-currencies-button',
                color="secondary",
                className="me-2"
            ),
            
            # Reset button (hidden initially)
            dbc.Button(
                "Show Current Rate",
                id='reset-button',
                color="primary",
                className="me-2",
                style={'display': 'none'}
            ),
            
            # Last updated info
            html.Div(id='last-updated-info', className="text-muted small mt-3")
        ])
    ], className="mb-4 shadow")


def _create_historical_card() -> dbc.Card:
    """Create the historical data card with chart.
    
    Returns:
        dbc.Card: Historical data card component
    """
    # Get default period from config
    default_period = config.get("ui", "default_period", 90)
    chart_height = config.get("ui", "chart_height", 400)
    
    return dbc.Card([
        dbc.CardHeader([
            html.H4("Historical Exchange Rates", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                # Period selector
                dbc.Col([
                    dbc.Label("Time Period:", html_for="period-selector"),
                    dcc.Dropdown(
                        id='period-selector',
                        options=[
                            {'label': '1 Week', 'value': 7},
                            {'label': '1 Month', 'value': 30},
                            {'label': '3 Months', 'value': 90},
                            {'label': '6 Months', 'value': 180},
                            {'label': '1 Year', 'value': 365},
                        ],
                        value=default_period,
                        clearable=False,
                        className="mb-3"
                    ),
                    html.Div(id='chart-info', className="text-muted small mt-2")
                ], md=3),
                
                # Chart
                dbc.Col([
                    dcc.Loading(
                        id="loading-chart",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='historical-chart',
                                config={'displayModeBar': True},
                                style={'height': f"{chart_height}px"}
                            )
                        ]
                    )
                ], md=9)
            ])
        ])
    ], className="mb-4 shadow")


def _create_footer() -> html.Footer:
    """Create the application footer.
    
    Returns:
        html.Footer: Footer component
    """
    return html.Footer([
        html.Hr(),
        html.P([
            "Data provided by the ",
            html.A("National Bank of Poland", href="https://nbp.pl/en/", target="_blank"),
            " API."
        ], className="text-center text-muted")
    ])


def _get_currency_options(data_handler: NBPDataHandler) -> List[Dict[str, str]]:
    """Generate currency dropdown options.
    
    Args:
        data_handler: Object providing currency rate data
        
    Returns:
        List[Dict[str, str]]: List of currency options for dropdowns
    """
    # Get current rates
    rates = data_handler.current_rates
    
    # Generate options with currency code and name
    options = []
    for code, rate_info in rates.items():
        if hasattr(rate_info, 'name') and rate_info.name:
            label = f"{code} - {rate_info.name}"
        else:
            label = code
            
        options.append({'label': label, 'value': code})
    
    # Sort by currency code
    return sorted(options, key=lambda x: x['value'])