# 💱 NBP Currency Converter

A web application for real-time currency conversion and historical exchange rate visualization using data from the National Bank of Poland (NBP) API.

## Features

- 🔄 Currency conversion with the latest exchange rates
- 📊 Interactive historical exchange rate charts
- 🔍 Support for all currencies published by NBP


## Installation
### From Source

```bash
# Clone the repository
git clone https://github.com/wowek2/programowanie/tree/main/semestr_2/lista_5
cd nbp_currency_converter

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

### Basic Usage

Once the application is running, open your web browser and navigate to:

```
http://localhost:8050
```

### Command Line Options

```bash
nbp-currency-converter --help
```

Options:
- `--config PATH`: Path to configuration file
- `--debug`: Run in debug mode
- `--port PORT`: Port to run the server on (default: 8050)
- `--theme THEME`: Theme to be used by application
### Configuration

You can customize the application behavior through config.py

## Project Structure

```
nbp_currency_converter/
├── app.py                  # Main application
├── config.py               # Configuration management
├── data/                   # Data handling modules
│   ├── handler.py          # NBP API data handler
│   └── models.py           # Data models
├── ui/                     # UI components
│   ├── callbacks.py        # Interactive callbacks
│   └── layout.py           # UI layout
└── utils/                  # Utility functions
    └── errors.py           # Custom exceptions
```

## Acknowledgments

- [National Bank of Poland](https://nbp.pl/en/) for providing the currency exchange rate API