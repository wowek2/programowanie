"""
Moduł do pobierania i przechowywania danych walutowych z API NBP.

Implementuje mechanizmy cache'owania i zarządzania danymi historycznymi.
"""

import requests
import requests_cache
from datetime import datetime, timedelta
import pandas as pd


class NBPDataHandler:
    """Klasa zarządzająca danymi z Narodowego Banku Polskiego.
    
    Attributes:
        current_rates (dict): Aktualne kursy walut
    """

    def __init__(self):
        requests_cache.install_cache(
            'nbp_cache',
            allowable_methods=('GET',),
            old_data_on_error=True
        )
        self._tables_cache = {
            'A': {'data': None, 'timestamp': None},
            'B': {'data': None, 'timestamp': None}
        }
        self._current_rates = None

    @property
    def current_rates(self) -> dict:
        """Property zwracająca aktualne kursy z automatyczną aktualizacją."""
        if self._should_refresh_rates():
            self._refresh_rates()
        return self._current_rates or self._get_cached_rates()

    def _should_refresh_rates(self) -> bool:
        """Sprawdza konieczność aktualizacji danych (co godzinę)."""
        if not self._current_rates:
            return True
        last_refresh = self._tables_cache['A']['timestamp'] or self._tables_cache['B']['timestamp']
        return (datetime.now() - last_refresh).seconds > 3600

    def _refresh_rates(self) -> None:
        """Pobiera i aktualizuje dane z tabel kursów A i B."""
        try:
            new_rates = {}
            table_a = self._fetch_table('A')
            if table_a:
                new_rates.update(self._process_table(table_a, 'A'))
                self._tables_cache['A'] = {'data': table_a, 'timestamp': datetime.now()}
            
            table_b = self._fetch_table('B')
            if table_b:
                new_rates.update(self._process_table(table_b, 'B'))
                self._tables_cache['B'] = {'data': table_b, 'timestamp': datetime.now()}
            
            new_rates['PLN'] = {'mid': 1.0, 'table': None}
            self._current_rates = new_rates
            
        except Exception as e:
            print(f"Błąd aktualizacji kursów: {e}. Używam zapisanych danych.")
            self._current_rates = self._get_cached_rates()

    def _fetch_table(self, table_code: str) -> dict:
        """Pobiera pojedynczą tabelę kursów z API NBP."""
        try:
            response = requests.get(
                f"http://api.nbp.pl/api/exchangerates/tables/{table_code}/",
                timeout=5
            )
            response.raise_for_status()
            return response.json()[0]
        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania tabeli {table_code}: {e}")
            return None

    def _get_cached_rates(self) -> dict:
        """Zwraca ostatnie poprawne dane z cache."""
        cached_rates = {}
        for table in ['A', 'B']:
            if self._tables_cache[table]['data']:
                cached_rates.update(
                    self._process_table(self._tables_cache[table]['data'], table))
        cached_rates['PLN'] = {'mid': 1.0, 'table': None}
        return cached_rates

    def _process_table(self, data: dict, table_code: str) -> dict:
        """Przetwarza surowe dane z API na format wewnętrzny."""
        return {rate['code']: {'mid': rate['mid'], 'table': table_code} for rate in data['rates']}

    def get_historical_series(self, currency: str, start_date_str: str, end_date_str: str) -> dict:
        """Pobiera historyczne dane kursowe dla wskazanej waluty.
        
        Args:
            currency (str): Kod waluty (np. 'USD')
            start_date_str (str): Data początkowa w formacie YYYY-MM-DD
            end_date_str (str): Data końcowa w formacie YYYY-MM-DD
            
        Returns:
            dict: Słownik z datami i kursami {data: kurs}
        """
        try:
            if currency == 'PLN':
                return self._generate_pln_series(start_date_str, end_date_str)
            
            table = self.current_rates.get(currency, {}).get('table', 'A')
            response = requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{start_date_str}/{end_date_str}/"
            )
            response.raise_for_status()
            return {entry['effectiveDate']: entry['mid'] for entry in response.json()['rates']}
            
        except Exception as e:
            print(f"Błąd danych historycznych: {e}. Brak danych w cache.")
            return {}

    def _generate_pln_series(self, start_date_str: str, end_date_str: str) -> dict:
        """Generuje dane dla PLN (kurs stały 1.0)."""
        start_date = datetime.fromisoformat(start_date_str).date()
        end_date = datetime.fromisoformat(end_date_str).date()
        dates = pd.bdate_range(start_date, end_date).strftime('%Y-%m-%d').tolist()
        return {date: 1.0 for date in dates}