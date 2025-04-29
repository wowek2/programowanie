"""
Data models for currency rates and historical data.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class CurrencyRate:
    """Model for a single currency exchange rate.
    
    Attributes:
        code: ISO currency code (e.g., 'USD')
        rate: Exchange rate to PLN
        table: NBP table identifier (A or B) or None for PLN
        name: Full currency name (optional)
        last_update: Last update date (optional)
    """
    code: str
    rate: float
    table: Optional[str]
    name: str = ""
    last_update: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            "code": self.code,
            "rate": self.rate,
            "table": self.table,
            "name": self.name,
            "last_update": self.last_update
        }


@dataclass
class HistoricalData:
    """Model for historical exchange rate data.
    
    Attributes:
        currency: ISO currency code (e.g., 'USD')
        dates: List of dates in ISO format
        rates: List of exchange rates corresponding to dates
        start_date: Query start date
        end_date: Query end date
    """
    currency: str
    dates: List[str]
    rates: List[float]
    start_date: str
    end_date: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            "currency": self.currency,
            "data": [{"date": date, "rate": rate} for date, rate in zip(self.dates, self.rates)],
            "start_date": self.start_date,
            "end_date": self.end_date
        }
    
    def to_series(self) -> Dict[str, float]:
        """Convert to date-rate dictionary.
        
        Returns:
            Dict[str, float]: Dictionary mapping dates to rates
        """
        return {date: rate for date, rate in zip(self.dates, self.rates)}