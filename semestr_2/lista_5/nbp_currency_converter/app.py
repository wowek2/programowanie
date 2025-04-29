"""
Main application module for the NBP Currency Converter.
"""

import logging
import argparse
from typing import Dict, Any, Optional

import dash
from dash import Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from config import config
from data.handler import NBPDataHandler
from ui.layout import create_layout
from ui.callbacks import register_callbacks


logger = logging.getLogger(__name__)

# Define available themes for the application
AVAILABLE_THEMES = {
    "LUX": dbc.themes.LUX,
    "BOOTSTRAP": dbc.themes.BOOTSTRAP,
    "CERULEAN": dbc.themes.CERULEAN,
    "COSMO": dbc.themes.COSMO,
    "CYBORG": dbc.themes.CYBORG,
    "DARKLY": dbc.themes.DARKLY,
    "FLATLY": dbc.themes.FLATLY,
    "JOURNAL": dbc.themes.JOURNAL,
    "LITERA": dbc.themes.LITERA,
    "LUMEN": dbc.themes.LUMEN,
    "MINTY": dbc.themes.MINTY,
    "MORPH": dbc.themes.MORPH,
    "PULSE": dbc.themes.PULSE,
    "QUARTZ": dbc.themes.QUARTZ,
    "SANDSTONE": dbc.themes.SANDSTONE,
    "SIMPLEX": dbc.themes.SIMPLEX,
    "SKETCHY": dbc.themes.SKETCHY,
    "SLATE": dbc.themes.SLATE,
    "SOLAR": dbc.themes.SOLAR,
    "SPACELAB": dbc.themes.SPACELAB,
    "SUPERHERO": dbc.themes.SUPERHERO,
    "UNITED": dbc.themes.UNITED,
    "VAPOR": dbc.themes.VAPOR,
    "YETI": dbc.themes.YETI,
    "ZEPHYR": dbc.themes.ZEPHYR
}


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="NBP Currency Converter")
    parser.add_argument(
        "--config", 
        type=str, 
        help="Path to configuration file"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Run in debug mode"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        help="Port to run the server on"
    )
    parser.add_argument(
        "--theme",
        type=str,
        choices=[theme.lower() for theme in AVAILABLE_THEMES.keys()],
        help=f"Visual theme for the application."
    )
    
    return parser.parse_args()


def create_app(
    data_handler: Optional[NBPDataHandler] = None,
    config_path: Optional[str] = None,
    theme_override: Optional[str] = None
) -> Dash:
    """Create and configure the Dash application.
    
    Args:
        data_handler: Optional pre-configured data handler
        config_path: Optional path to configuration file
        theme_override: Optional theme to override config setting
        
    Returns:
        Dash: Configured Dash application
    """
    # Update configuration if config file provided
    if config_path:
        from nbp_currency_converter.config import Config
        global config
        config = Config(config_path)
    
    # Create data handler if not provided
    if not data_handler:
        data_handler = NBPDataHandler()
    
    # Get theme from override or config
    if theme_override:
        theme_name = theme_override.upper()
    else:
        theme_name = config.get("app", "theme", "LUX").upper()
    
    # Get theme or fallback to LUX
    bootstrap_theme = AVAILABLE_THEMES.get(theme_name, dbc.themes.LUX)
    
    # Initialize Dash application
    app = Dash(
        __name__,
        external_stylesheets=[
            bootstrap_theme,
            dbc.icons.BOOTSTRAP
        ],
        title=config.get("app", "title", "NBP Currency Converter"),
        suppress_callback_exceptions=True,
        update_title=None
    )
    
    # Load matching figure template for charts
    try:
        load_figure_template(theme_name.lower())
    except ValueError:
        # If the template isn't available, use a default one
        load_figure_template("lux")
    
    # Set application layout
    app.layout = create_layout(data_handler)
    
    # Register interactive callbacks
    register_callbacks(app, data_handler)
    
    return app


def run_server():
    """Run the Dash application server.
    
    This function is the entry point for running the application.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Create and configure application
    app = create_app(
        config_path=args.config,
        theme_override=args.theme
    )
    
    # Determine server settings
    debug = args.debug if args.debug is not None else config.get("app", "debug", False)
    host = config.get("app", "host", "0.0.0.0")
    port = args.port or config.get("app", "port", 8050)
    
    # Log startup information
    logger.info(f"Starting NBP Currency Converter on {host}:{port} (debug={debug})")
    if args.theme:
        logger.info(f"Using theme: {args.theme.upper()}")
    
    # Run server
    app.run(
        debug=debug,
        host=host,
        port=port
    )


app = create_app()
server = app.server

if __name__ == '__main__':
    """Main entry point for running the application."""
    run_server()