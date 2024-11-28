"""
## WebLocalization
Submodule of PyLocalizer by MF366
"""

from ._internal.JSONLocalization import JSONLocalization
from typing import Any
import requests


class WebLocalization:
    def __init__(self, formatting: Any, url: str, *, encoding: str = 'utf-8'):
        self._formatting: Any = formatting
        self._cur_language_url: str = url
        self._cur_language_data: dict[str, str] = {}
        self.__inner_localizer = JSONLocalization(formatting, url)
    
    def get_entry_value(self, entry: str, *, in_case_of_error: str | None = None) -> str:
        return self.__inner_localizer.get_entry_value(entry, in_case_of_error=in_case_of_error)
    
    def change_language(self, language_url: str, timeout: float = 1, allow_redirects: bool = False):
        response = requests.get(language_url, timeout=timeout, allow_redirects=allow_redirects)
        
        if response.status_code != 200:
            raise ValueError(f'{language_url} cannot be accessed right now')
        
        self._cur_language_url = language_url
        self._cur_language_data = response.json()
        self.__inner_localizer._cur_language_data = self._cur_language_data
        
    def format_entry_value(self, entry_value: str, **additional_values) -> str:
        return self.__inner_localizer.format_entry_value(entry_value, **additional_values)
    
    def get_formatted_entry(self, entry: str, **kw) -> str:
        """
        ## WebLocalization.get_formatted_entry
        Gets and formats an entry. If there is nothing to format, the function will simply get the wanted entry.

        :param entry: the entry to get and to (possibly) format *(str)*
        :return: the entry, formatted if there was anything to format
        
        ### About **kw
        You can set additional formatting values like in `format_entry_value`. You can also use special argument `in_case_of_error` for `get_entry_value`.
        """
        
        return self.__inner_localizer.get_formatted_entry(entry, **kw)
    
    def __getitem__(self, entry: str) -> str:
        return self.get_formatted_entry(entry) # [i] simple use of get_formatted_entry: no special entries and no if error cases
    
    def __str__(self) -> str:
        return self._cur_language_url
