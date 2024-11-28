"""
## RawLocalization
Submodule of PyLocalizer by MF366
"""

from typing import Any


class RawLocalization:
    def __init__(self, formatting: Any, default_language: str, separator: str, *, encoding: str = 'utf-8'):
        if len(separator) != 1:
            raise ValueError('the separator must be exactly one character long')
        
        self._formatting: Any = formatting
        self._SEPARATOR: str = separator
        self._cur_language_file: str = default_language
        self.__eggs: str = ""
        self._cur_language_data: dict[str, str] = {}
        self._ENCODING: str = encoding
    
    def __build_dict_from_raw(self):
        if not self.__eggs:
            return # [!] abort as __eggs is empty
        
        spam: list[str] = self.__eggs.split('\n')
        
        for value in spam:
            foo: list[str] = value.split('=')
            self._cur_language_data[foo[0].split()] = foo[1]        
    
    def get_entry_value(self, entry: str, *, in_case_of_error: str | None = None) -> str:
        if in_case_of_error:
            return self._cur_language_data.get(entry, in_case_of_error)
        
        return self._cur_language_data[entry]
    
    def change_language(self, new_language: str):
        self._cur_language_file = new_language
        
        with open(self._cur_language_file, "r", encoding=self._ENCODING) as f:
            self.__eggs = f.read()
            
        self.__build_dict_from_raw()
        
    def format_entry_value(self, entry_value: str, **additional_values) -> str:
        vals: dict[str, str] = self._formatting.entries
        
        if len(additional_values) != 0:
            for v, k in additional_values.items():
                vals[v] = k # [i] give priority to additonal values if there are any
                # [i] otherwise, the formatting values will be used even if there isn't a single value
            
        return entry_value.format(**vals)
    
    def get_formatted_entry(self, entry: str, **kw) -> str:
        """
        ## RawLocalization.get_formatted_entry
        Gets and formats an entry. If there is nothing to format, the function will simply get the wanted entry.

        :param entry: the entry to get and to (possibly) format *(str)*
        :return: the entry, formatted if there was anything to format
        
        ### About **kw
        You can set additional formatting values like in `format_entry_value`. You can also use special argument `in_case_of_error` for `get_entry_value`.
        """
        
        in_case_of_error: Any = kw.pop('in_case_of_error', None)
        
        entry_value: str = self.get_entry_value(entry, in_case_of_error=in_case_of_error)
        
        if entry_value == in_case_of_error:
            # [!] there was an error; don't proceed with formatting
            return entry_value
        
        if entry_value.count('{') > 0 and entry_value.count('}') > 0:
            # [i] there is something to format!! :D
            entry_value = self.format_entry_value(entry_value, **kw)
            
        return entry_value
    
    @property
    def encoding(self) -> str:
        return self._ENCODING
    
    def __getitem__(self, entry: str) -> str:
        return self.get_formatted_entry(entry) # [i] simple use of get_formatted_entry: no special entries and no if error cases
    
    def __str__(self) -> str:
        return self._cur_language_file
