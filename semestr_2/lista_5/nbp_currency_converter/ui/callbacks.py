"""
Module implementing the interactive logic and UI for the application.
"""

import logging
from datetime import date, timedelta
from typing import Dict, List, Any, Tuple, Optional

import dash
from dash import Input, Output, State, callback, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from config import config
from data.handler import NBPDataHandler
from utils.errors import NBPError, DataFetchError

# Set up logger
logger = logging.getLogger(__name__)


def register_callbacks(app: dash.Dash, data_handler: NBPDataHandler) -> None:
    """Register all callbacks for the Dash application.

    Args:
        app: Dash application instance
        data_handler: Object for managing currency data
    """
    # Application state callbacks
    _register_state_callbacks(app, data_handler)
    
    # Currency converter callbacks
    _register_converter_callbacks(app, data_handler)
    
    # Historical chart callbacks
    _register_chart_callbacks(app, data_handler)


def _register_state_callbacks(app: dash.Dash, data_handler: NBPDataHandler) -> None:
    """Register callbacks for managing application state.
    
    Args:
        app: Dash application instance
        data_handler: Object for managing currency data
    """
    @app.callback(
        Output('app-state', 'data'),
        [
            Input('reset-button', 'n_clicks'),
            Input('historical-chart', 'clickData'),
            Input('from-currency-dropdown', 'value'),
            Input('to-currency-dropdown', 'value')
        ],
        [State('app-state', 'data')]
    )
    def update_app_state(reset_clicks, chart_click_data, from_currency, to_currency, current_state):
        """Update the application state based on user interactions.
        
        The app can be in two main states:
        1. Using current rates for conversion
        2. Using historical rates from a chart click
        
        Args:
            reset_clicks: Number of clicks on reset button
            chart_click_data: Click data from the chart
            from_currency: Selected source currency
            to_currency: Selected target currency
            current_state: Current application state
            
        Returns:
            Dict: Updated application state
        """
        # Create a copy of current state to avoid modifying it directly
        new_state = dict(current_state or {})
        
        # Check which input triggered the callback
        ctx = dash.callback_context
        if not ctx.triggered:
            return current_state
            
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Handle different triggers
        if trigger_id == 'reset-button':
            new_state['use_current'] = True
            new_state.pop('selected_date', None)
            new_state.pop('selected_rate', None)
        
        elif trigger_id == 'historical-chart' and chart_click_data:
            point = chart_click_data['points'][0]
            new_state['use_current'] = False
            new_state['selected_date'] = point['x']
            new_state['selected_rate'] = point['y']
        
        elif trigger_id in ('from-currency-dropdown', 'to-currency-dropdown'):
            # When currencies change, reset to current rates
            if 'selected_date' in new_state:
                new_state['use_current'] = True
                new_state.pop('selected_date', None)
                new_state.pop('selected_rate', None)
            
        return new_state


def _register_converter_callbacks(app: dash.Dash, data_handler: NBPDataHandler) -> None:
    """Register callbacks for the currency converter.
    
    Args:
        app: Dash application instance
        data_handler: Object for managing currency data
    """
    @app.callback(
        [
            Output('conversion-result', 'children'),
            Output('reset-button', 'style'),
            Output('last-updated-info', 'children')
        ],
        [
            Input('app-state', 'data'),
            Input('amount-input', 'value'),
            Input('from-currency-dropdown', 'value'),
            Input('to-currency-dropdown', 'value')
        ]
    )
    def update_conversion_result(state, amount, from_currency, to_currency):
        """Update the conversion result based on inputs and app state.
        
        Args:
            state: Application state
            amount: Amount to convert
            from_currency: Source currency
            to_currency: Target currency
            
        Returns:
            Tuple: (conversion result component, reset button style, last updated info)
        """
        # Input validation
        if not amount or amount <= 0:
            return (
                dbc.Alert("Please enter a valid amount", color="warning"),
                {'display': 'none'},
                ""
            )
            
        if from_currency == to_currency:
            return (
                dbc.Alert(f"{amount} {from_currency} = {amount} {to_currency}", color="info"),
                {'display': 'none'},
                ""
            )
            
        # Get application state
        use_current = state.get('use_current', True)
        selected_date = state.get('selected_date')
        selected_rate = state.get('selected_rate')
        
        try:
            if use_current:
                # Use current rates (always fetched directly from the API)
                rate = data_handler.get_currency_pair_rate(from_currency, to_currency)
                converted = amount * rate
                
                # Get last update time
                last_update = ""
                for code in (from_currency, to_currency):
                    if code in data_handler.current_rates and hasattr(data_handler.current_rates[code], 'last_update'):
                        last_update = f"Last updated: {data_handler.current_rates[code].last_update}"
                        break
                        
                return (
                    dbc.Alert(
                        [
                            html.Span(f"{amount} {from_currency} = ", className="me-1"),
                            html.Strong(f"{converted:.4f} {to_currency}", className="fs-5")
                        ],
                        color="success"
                    ),
                    {'display': 'none'},
                    last_update
                )
                
            else:
                # Use historical rate from chart click
                if not selected_date or selected_rate is None:
                    return (
                        dbc.Alert("Click on the chart to see historical conversion rates", color="info"),
                        {'display': 'none'},
                        ""
                    )
                
                converted = amount * selected_rate
                
                return (
                    dbc.Alert(
                        [
                            html.Span(f"On {selected_date}: {amount} {from_currency} = ", className="me-1"),
                            html.Strong(f"{converted:.4f} {to_currency}", className="fs-5")
                        ],
                        color="info"
                    ),
                    {'display': 'block'},
                    ""
                )
                
        except ValueError as e:
            return (
                dbc.Alert(f"Error: {str(e)}", color="danger"),
                {'display': 'none'},
                ""
            )
        except NBPError as e:
            return (
                dbc.Alert(f"API Error: {e.message}", color="danger"),
                {'display': 'none'},
                ""
            )
        except Exception as e:
            logger.exception("Unexpected error in conversion")
            return (
                dbc.Alert("An unexpected error occurred", color="danger"),
                {'display': 'none'},
                ""
            )
            
    @app.callback(
        [
            Output('from-currency-dropdown', 'value'),
            Output('to-currency-dropdown', 'value')
        ],
        Input('swap-currencies-button', 'n_clicks'),
        [
            State('from-currency-dropdown', 'value'),
            State('to-currency-dropdown', 'value')
        ]
    )
    def swap_currencies(n_clicks, from_currency, to_currency):
        """Swap the selected currencies when the swap button is clicked.
        
        Args:
            n_clicks: Number of button clicks
            from_currency: Current source currency
            to_currency: Current target currency
            
        Returns:
            Tuple: (new source currency, new target currency)
        """
        if n_clicks is None:
            # Initial load, don't swap
            return dash.no_update, dash.no_update
            
        return to_currency, from_currency


def _register_chart_callbacks(app: dash.Dash, data_handler: NBPDataHandler) -> None:
    """Register callbacks for the historical chart.
    
    Args:
        app: Dash application instance
        data_handler: Object for managing currency data
    """
    @app.callback(
        [
            Output('historical-chart', 'figure'),
            Output('chart-info', 'children')
        ],
        [
            Input('from-currency-dropdown', 'value'),
            Input('to-currency-dropdown', 'value'),
            Input('period-selector', 'value')
        ]
    )
    def update_historical_chart(from_currency, to_currency, days):
        """Update the historical exchange rate chart.
        
        Args:
            from_currency: Source currency
            to_currency: Target currency
            days: Number of days to show
            
        Returns:
            Tuple: (chart figure, chart info text)
        """
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=int(days))
        
        try:
            # Get historical data for both currencies (always fetched directly from the API)
            from_data = data_handler.get_historical_series(
                from_currency,
                start_date.isoformat(),
                end_date.isoformat()
            )
            
            to_data = data_handler.get_historical_series(
                to_currency,
                start_date.isoformat(),
                end_date.isoformat()
            )
            
            # Convert to dictionaries for easier processing
            from_series = from_data.to_series()
            to_series = to_data.to_series()
            
            # Find common dates between both series
            common_dates = sorted(set(from_series) & set(to_series))
            
            if not common_dates:
                # No data available
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title=f"No data available for {from_currency}/{to_currency}",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    annotations=[
                        dict(
                            text="No historical data available for this period",
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=16)
                        )
                    ],
                    height=config.get("ui", "chart_height", 400)
                )
                return empty_fig, "No data available for the selected period"
            
            # Calculate conversion rates
            rates = []
            for date_str in common_dates:
                rate = from_series[date_str] / to_series[date_str]
                rates.append(rate)
            
            # Create chart data
            chart_data = {
                "Date": common_dates,
                "Rate": rates
            }
            
            # Create figure
            fig = px.line(
                chart_data,
                x="Date",
                y="Rate",
                labels={"Rate": f"{from_currency}/{to_currency} Rate"},
                title=f"{from_currency}/{to_currency} Exchange Rate"
            )
            
            # Customize figure
            fig.update_layout(
                hovermode="x unified",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12
                ),
                margin=dict(l=40, r=40, t=50, b=40),
                height=config.get("ui", "chart_height", 400),
                xaxis=dict(
                    title="",
                    tickformat="%Y-%m-%d",
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.1)"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.1)"
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                transition_duration=config.get("ui", "animate_charts", True) and 500 or 0
            )
            
            # Add markers
            fig.update_traces(
                mode="lines+markers",
                marker=dict(size=6),
                line=dict(width=3),
                hovertemplate="%{y:.4f}"
            )
            
            # Calculate statistics for info panel
            min_rate = min(rates)
            max_rate = max(rates)
            avg_rate = sum(rates) / len(rates)
            
            info_text = [
                f"Min: {min_rate:.4f}",
                f"Max: {max_rate:.4f}",
                f"Avg: {avg_rate:.4f}",
                f"Period: {start_date.isoformat()} to {end_date.isoformat()}"
            ]
            
            return fig, html.Div([html.Div(t) for t in info_text])
            
        except NBPError as e:
            # Handle API errors
            empty_fig = go.Figure()
            empty_fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                annotations=[
                    dict(
                        text=f"API Error: {e.message}",
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(color="red", size=16)
                    )
                ],
                height=config.get("ui", "chart_height", 400)
            )
            return empty_fig, f"Error: {e.message}"
            
        except Exception as e:
            # Handle unexpected errors
            logger.exception("Unexpected error in chart generation")
            empty_fig = go.Figure()
            empty_fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                annotations=[
                    dict(
                        text="An error occurred while generating the chart",
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(color="red", size=16)
                    )
                ],
                height=config.get("ui", "chart_height", 400)
            )
            return empty_fig, "An unexpected error occurred"