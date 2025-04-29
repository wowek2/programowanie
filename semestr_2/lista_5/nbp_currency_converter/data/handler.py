"""
Module for fetching and processing currency data from the NBP API.
"""

from typing import Dict, Optional, List, Any
import logging

import pandas as pd
import requests

from data.models import CurrencyRate, HistoricalData
from utils.errors import NBPApiError, DataFetchError

# Setup logging
logger = logging.getLogger(__name__)


class NBPDataHandler:
    """Class for managing currency data from the National Bank of Poland.
    """

    def __init__(self):
        """Initialize the NBP data handler."""
        # We'll only keep the last fetched rates in memory
        self._current_rates: Optional[Dict[str, CurrencyRate]] = None

    @property
    def current_rates(self) -> Dict[str, CurrencyRate]:
        """Get the latest exchange rates.
        
        Returns:
            Dict[str, CurrencyRate]: Dictionary of currency codes to rate information
        """
        # Always fetch fresh data
        try:
            self._fetch_current_rates()
        except Exception as e:
            logger.error(f"Error fetching current rates: {e}")
            if not self._current_rates:
                raise DataFetchError("Failed to fetch currency rates")
                
        return self._current_rates or {}

    def _fetch_current_rates(self) -> None:
        """Fetch the latest exchange rates from NBP API tables A and B."""
        try:
            new_rates: Dict[str, CurrencyRate] = {}
            
            # Fetch and process Table A (main currencies)
            table_a = self._fetch_table('A')
            if table_a:
                new_rates.update(self._process_table(table_a, 'A'))
            
            # Fetch and process Table B (exotic currencies)
            table_b = self._fetch_table('B')
            if table_b:
                new_rates.update(self._process_table(table_b, 'B'))
            
            # Add PLN as base currency (always 1.0)
            new_rates['PLN'] = CurrencyRate(code='PLN', rate=1.0, table=None)
            
            # Update current rates
            self._current_rates = new_rates
            
        except Exception as e:
            logger.error(f"Error fetching rates: {e}")
            raise DataFetchError(f"Failed to fetch currency rates: {str(e)}")

    def _fetch_table(self, table_code: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific exchange rate table from NBP API.
        
        Args:
            table_code: Table code ('A' or 'B')
            
        Returns:
            Optional[Dict[str, Any]]: Table data or None if fetch failed
            
        Raises:
            NBPApiError: If API returns an error response
        """
        try:
            response = requests.get(
                f"http://api.nbp.pl/api/exchangerates/tables/{table_code}/",
                headers={"Accept": "application/json"},
                timeout=10
            )
            
            if response.status_code == 404:
                logger.warning(f"Table {table_code} not found")
                return None
                
            response.raise_for_status()
            return response.json()[0]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching table {table_code}: {e}")
            
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code >= 400:
                raise NBPApiError(f"NBP API error: {e}")
                
            return None

    def _process_table(self, data: Dict[str, Any], table_code: str) -> Dict[str, CurrencyRate]:
        """Process raw API data into internal format.
        
        Args:
            data: Raw API response data
            table_code: Table code ('A' or 'B')
            
        Returns:
            Dict[str, CurrencyRate]: Dictionary of currency codes to rate information
        """
        return {
            rate['code']: CurrencyRate(
                code=rate['code'],
                rate=rate['mid'],
                table=table_code,
                name=rate.get('currency', ''),
                last_update=data.get('effectiveDate')
            ) 
            for rate in data['rates']
        }

    def get_historical_series(self, currency: str, start_date: str, end_date: str) -> HistoricalData:
        """Get historical exchange rates for a specific currency.
        
        Args:
            currency: Currency code (e.g. 'USD')
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
            
        Returns:
            HistoricalData: Historical rates data with dates and rates
            
        Raises:
            NBPApiError: If API returns an error response
            DataFetchError: If data fetching fails
        """
        try:
            # Special case for PLN (always 1.0)
            if currency == 'PLN':
                return self._generate_pln_series(start_date, end_date)
            
            # Get table type for the currency
            table = self._get_currency_table(currency)
            
            # Fetch historical data from NBP API
            url = f"http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{start_date}/{end_date}/"
            response = requests.get(
                url,
                headers={"Accept": "application/json"},
                timeout=15
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Process and return historical data
            dates = [entry['effectiveDate'] for entry in data['rates']]
            rates = [entry['mid'] for entry in data['rates']]
            
            return HistoricalData(
                currency=currency,
                dates=dates,
                rates=rates,
                start_date=start_date,
                end_date=end_date
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching historical data for {currency}: {e}")
            
            if isinstance(e, requests.exceptions.HTTPError):
                if e.response.status_code == 404:
                    # Handle 404 error (no data for the specified period)
                    logger.warning(f"No historical data for {currency} in period {start_date} - {end_date}")
                    return HistoricalData(
                        currency=currency,
                        dates=[],
                        rates=[],
                        start_date=start_date,
                        end_date=end_date
                    )
                else:
                    raise NBPApiError(f"NBP API error: {e}")
            
            raise DataFetchError(f"Failed to fetch historical data for {currency}: {e}")

    def _get_currency_table(self, currency: str) -> str:
        """Determine which NBP table a currency belongs to.
        
        Args:
            currency: Currency code
            
        Returns:
            str: Table code ('A' or 'B')
        """
        # Fetch current rates to ensure we have the latest information
        rates = self.current_rates
        
        if currency in rates and rates[currency].table:
            return rates[currency].table
        
        # Default to table A if not found
        return 'A'

    def _generate_pln_series(self, start_date: str, end_date: str) -> HistoricalData:
        """Generate historical data for PLN (always 1.0).
        
        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
            
        Returns:
            HistoricalData: Historical rates data for PLN
        """
        try:
            # Generate business days between start and end dates
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            date_range = pd.bdate_range(start=start, end=end)
            
            # Format dates and create a list of 1.0 rates
            dates = date_range.strftime('%Y-%m-%d').tolist()
            rates = [1.0] * len(dates)
            
            return HistoricalData(
                currency='PLN',
                dates=dates,
                rates=rates,
                start_date=start_date,
                end_date=end_date
            )
            
        except Exception as e:
            logger.error(f"Error generating PLN series: {e}")
            return HistoricalData(
                currency='PLN',
                dates=[],
                rates=[],
                start_date=start_date,
                end_date=end_date
            )
            
    def get_currency_pair_rate(self, from_currency: str, to_currency: str) -> float:
        """Calculate exchange rate between two currencies.
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            float: Exchange rate from source to target currency
            
        Raises:
            ValueError: If currency codes are invalid
        """
        # Always fetch fresh rates
        current_rates = self.current_rates
        
        if from_currency not in current_rates:
            raise ValueError(f"Invalid source currency: {from_currency}")
            
        if to_currency not in current_rates:
            raise ValueError(f"Invalid target currency: {to_currency}")
            
        # Calculate the rate (using PLN as an intermediate)
        rate_from = current_rates[from_currency].rate
        rate_to = current_rates[to_currency].rate
        
        return rate_from / rate_to