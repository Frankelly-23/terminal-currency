import curses
import random

class Currencyscr:
    def __init__(self, currencies: list[list[str]], title: str, nlines: int, ncols: int, beginY: int, beginX: int, color: list[int]):
        self.currencies: list[list[str]] = currencies 
        self.title: str = title
        self.color: list[int]= color
        self.currencyscr: curses.window = curses.newwin(nlines, ncols, beginY, beginX)
        
        self.height, self.width = self.currencyscr.getmaxyx()
        self.title_x: int = max(0, (self.width - len(self.title)) // 2)
        self.title_y: int = self.height // 5
        self.content_y_start: int = self.title_y + 2


    def write_currency(self):
        self.currencyscr.erase()
        self.currencyscr.box()
        
        self.currencyscr.addstr(self.title_y, self.title_x, self.title, self.color[0])

        # Draw currencies
        for i, currency in enumerate(self.currencies):
            if self.content_y_start + i >= self.height - 1:
                break
            x = max(0, (self.width - len(currency[0])) // 2)
            self.currencyscr.addstr(self.content_y_start + i, x, f"{currency[0]} €") 
        
        self.currencyscr.noutrefresh()

    def chart_mode(self):
        self.currencyscr.erase()
        
        self.currencyscr.addstr(self.title_y, self.title_x, self.title, self.color[0])
        
        for i, currency in enumerate(self.currencies):
            code = currency[1] 
            currency_value = int(currency[2])
            code_and_value = f" {code} {currency_value} "
            chart_char = "|" 
            if len(chart_char * currency_value) + len(code_and_value) >= self.width - 6:
                chart_to_display = f"{chart_char * (self.width - len(code_and_value))}{code_and_value}"
            else:
                chart_to_display = f"{chart_char * currency_value}{code_and_value}"

            self.currencyscr.addstr(self.content_y_start + i, 1, chart_to_display, self.color[random.randint(0, len(self.color) - 1)]) 
        self.currencyscr.noutrefresh()





