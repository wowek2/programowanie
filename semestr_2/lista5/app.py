"""
Główny moduł aplikacji Dash do przeliczania walut z wykorzystaniem danych NBP.

Moduł inicjalizuje aplikację, integruje komponenty i uruchamia serwer.
"""

import dash
from dash import Dash
import dash_bootstrap_components as dbc
from data_handler import NBPDataHandler
from layout import create_layout
from callbacks import register_callbacks


def create_app() -> Dash:
    """Fabryka aplikacji Dash inicjalizująca komponenty i konfigurująca layout.

    Returns:
        Dash: Gotowa do uruchomienia instancja aplikacji Dash.
    """
    # Inicjalizacja data handlera
    data_handler = NBPDataHandler()
    
    # Inicjalizacja Dash'a
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    server = app.server

    
    # Konfiguracja layotu i callbacków
    app.layout = create_layout(data_handler)
    register_callbacks(app, data_handler)
    
    return app


if __name__ == '__main__':
    """Główny punkt wejścia uruchamiający aplikację."""
    app = create_app()
    app.run(debug=True)