"""
Moduł callbacków implementujący logikę interaktywną aplikacji.

Zawiera funkcje aktualizujące dane, wyniki konwersji i wykres historyczny.
"""

import dash
from dash import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date, timedelta


def register_callbacks(app: dash.Dash, data_handler) -> None:
    """Rejestruje wszystkie callbacki w aplikacji Dash.

    Args:
        app (dash.Dash): Instancja aplikacji Dash
        data_handler: Obiekt do zarządzania danymi walut
    """

    @app.callback(
        Output('store', 'data'),
        [Input('reset_button', 'n_clicks'),
         Input('history_graph', 'clickData'),
         Input('from_currency', 'value'),
         Input('to_currency', 'value')],
        [State('store', 'data')]
    )
    def update_store(n_clicks, click_data, *args):
        """Aktualizuje stan przechowywany w dcc.Store.
        
        Obsługuje resetowanie stanu i przełączanie między aktualnymi/historycznymi kursami.
        """
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
            
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if triggered_id == 'reset_button':
            return {'use_current': True}
        elif triggered_id == 'history_graph':
            return {'use_current': False}
        else:
            return dash.no_update

    @app.callback(
        [Output('output', 'children'),
         Output('reset_button', 'style')],
        [Input('store', 'data'),
         Input('history_graph', 'clickData'),
         Input('amount', 'value')],
        [State('from_currency', 'value'),
         State('to_currency', 'value')]
    )
    def update_output(store_data, click_data, amount, from_curr, to_curr):
        """Aktualizuje panel na podstawie wybranych parametrów."""
        use_current = store_data.get('use_current', True)

        # Walidacja danych wejściowych
        if not amount or amount <= 0:
            return dbc.Alert("Wprowadź poprawną kwotę", color="danger"), {'display': 'none'}
        
        if use_current:
            rate_from = data_handler.current_rates.get(from_curr, {}).get('mid')
            rate_to = data_handler.current_rates.get(to_curr, {}).get('mid')
            
            if None in (rate_from, rate_to):
                return dbc.Alert("Nieprwidłowa waluta", color="danger"), {'display': 'none'}
            
            converted = amount * (rate_from / rate_to)
            return (
                dbc.Alert(f"Aktualny kurs: {amount} {from_curr} = {converted:.4f} {to_curr}", color="success"),
                {'display': 'none'}
            )
        else:
            if not click_data:
                # Logika dla danych historycznych
                return dbc.Alert("Kliknij na wykres aby zobaczyć historyczny kurs", color="info"), {'display': 'none'}
            
            point = click_data['points'][0]
            date = point['x']
            rate = point['y']
            converted = amount * rate
            return (
                dbc.Alert(f"Historyczny kurs w dniu {date}: {amount} {from_curr} = {converted:.4f} {to_curr}", color="info"),
                {'display': 'block', 'marginTop': '10px'}
            )            
            rate_from = data_handler.current_rates.get(from_curr, {}).get('mid')
            rate_to = data_handler.current_rates.get(to_curr, {}).get('mid')
            
            if None in (rate_from, rate_to):
                return dbc.Alert("Nieprwidłowa waluta", color="danger"), {'display': 'none'}
            
            converted = amount * (rate_from / rate_to)
            return (
                dbc.Alert(f"Aktualny kurs: {amount} {from_curr} = {converted:.4f} {to_curr}", color="success"),
                {'display': 'none'}
            )

    @app.callback(
        Output('history_graph', 'figure'),
        [Input('from_currency', 'value'),
        Input('to_currency', 'value'),
        Input('period_selector', 'value')]
    )
    def update_graph(from_curr, to_curr, days):
        """Generuje wykres historycznych kursów dla wybranej pary walutowej."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        series_from = data_handler.get_historical_series(
            from_curr,
            start_date.isoformat(),
            end_date.isoformat()
        )
        series_to = data_handler.get_historical_series(
            to_curr,
            start_date.isoformat(),
            end_date.isoformat()
        )
        
        common_dates = sorted(set(series_from) & set(series_to))
        
        if not common_dates or not series_from or not series_to:
            return {
                'data': [],
                'layout': {
                    'title': None,
                    'xaxis': {'visible': False},
                    'yaxis': {'visible': False},
                    'annotations': [{
                        'text': 'Nie udało się uzyskać informacji',
                        'xref': 'paper',
                        'yref': 'paper',
                        'x': 0.5,
                        'y': 0.5,
                        'showarrow': False,
                        'font': {'size': 24, 'color': 'red'}
                    }],
                    'height': 400
                }
            }
        
        conversion = [series_from[d] / series_to[d] for d in common_dates]
        
        fig = px.line(
            x=common_dates,
            y=conversion,
            labels={'x': '', 'y': f'{from_curr}/{to_curr}'},
            height=400
        )
        fig.update_layout(
            margin=dict(t=30, b=20, l=40, r=20),
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_showgrid=False,
            yaxis_showgrid=False
        )
        return fig