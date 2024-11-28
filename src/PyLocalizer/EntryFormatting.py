"""
## EntryFormatting
Submodule of PyLocalizer by MF366
"""

import colorama


class EntryFormatter:
    def __init__(self, import_colorama_foreground: bool = True, import_colorama_background: bool = False, import_colorama_styles: bool = True, **entries):
        self.__entries = {}
        
        if import_colorama_foreground:
            for i in dir(colorama.Fore):
                if i.startswith('__'):
                    continue
                
                self.__entries[f'Fore.{i}'] = eval(f"colorama.Fore.{i}")
                
        if import_colorama_background:
            for i in dir(colorama.Back):
                if i.startswith('__'):
                    continue
                
                self.__entries[f'Back.{i}'] = eval(f"colorama.Back.{i}")
                
        if import_colorama_styles:
            for i in dir(colorama.Style):
                if i.startswith('__'):
                    continue
                
                self.__entries[f'Style.{i}'] = eval(f"colorama.Style.{i}")
                
        self.__entries['reset'] = colorama.Style.RESET_ALL
        
        for k, v in entries.items():
            self.__entries[k.strip()] = v
                
    @property
    def entries(self):
        return self.__entries
