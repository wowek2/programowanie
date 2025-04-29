"""
Custom exceptions for the NBP Currency Converter application.
"""


class NBPError(Exception):
    """Base exception class for all NBP Currency Converter errors."""
    
    def __init__(self, message: str = "An error occurred", *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class NBPApiError(NBPError):
    """Exception raised when the NBP API returns an error.
    
    Attributes:
        message: Error message
        status_code: HTTP status code (if available)
        endpoint: API endpoint that caused the error (if available)
    """
    
    def __init__(self, message: str, status_code: int = None, endpoint: str = None):
        self.status_code = status_code
        self.endpoint = endpoint
        super().__init__(message)
        
    def __str__(self):
        base_msg = self.message
        
        if self.status_code:
            base_msg += f" (Status code: {self.status_code})"
            
        if self.endpoint:
            base_msg += f" while accessing {self.endpoint}"
            
        return base_msg


class DataFetchError(NBPError):
    """Exception raised when data fetching fails.
    
    Attributes:
        message: Error message
        currency: Currency code (if applicable)
    """
    
    def __init__(self, message: str, currency: str = None):
        self.currency = currency
        super().__init__(message)
        
    def __str__(self):
        if self.currency:
            return f"{self.message} for currency {self.currency}"
        return self.message


class CurrencyConversionError(NBPError):
    """Exception raised when currency conversion fails.
    
    Attributes:
        message: Error message
        from_currency: Source currency code
        to_currency: Target currency code
    """
    
    def __init__(self, message: str, from_currency: str = None, to_currency: str = None):
        self.from_currency = from_currency
        self.to_currency = to_currency
        super().__init__(message)
        
    def __str__(self):
        if self.from_currency and self.to_currency:
            return f"{self.message} for conversion from {self.from_currency} to {self.to_currency}"
        return self.message


class ConfigurationError(NBPError):
    """Exception raised when application configuration is invalid.
    
    Attributes:
        message: Error message
        parameter: Configuration parameter that caused the error (if available)
    """
    
    def __init__(self, message: str, parameter: str = None):
        self.parameter = parameter
        super().__init__(message)
        
    def __str__(self):
        if self.parameter:
            return f"{self.message} (parameter: {self.parameter})"
        return self.message