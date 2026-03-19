import curses

class Currencyscr:
    def __init__(self, 
            currencies: list[tuple[str, str, float]], 
            title: str, 
            nlines: int, 
            ncols: int, 
            beginY: int, 
            beginX: int, 
            colors: list[int]
                 ):

        self.currencies: list[tuple[str, str, float]] = currencies 
        self.title: str = title
        self.colors: list[int]= colors
        self.currencyscr: curses.window = curses.newwin(nlines, ncols, beginY, beginX)
        
        self.height, self.width = self.currencyscr.getmaxyx()
        self.title_x: int = max(0, (self.width - len(self.title)) // 2)
        self.title_y: int = self.height // 5
        self.content_y_start: int = self.title_y + 2
       

    def _decide_color(self, value: float):
        low: int = 20
        medium: int = 100
        # RED MAGENTA GREEN 
        if value < low:
            return self.colors[0]
        elif value < medium:
           return self.colors[1]
        else:
            return self.colors[2]

    def _add_titles(self):
        self.currencyscr.erase()
        self.currencyscr.addstr(self.title_y, self.title_x, self.title)

    def write_currency(self):
        self._add_titles()
        self.currencyscr.box()
        
        # Draw currencies
        for i, currency in enumerate(self.currencies):
            if self.content_y_start + i >= self.height - 1:
                break
            x = max(0, (self.width - len(currency[0])) // 2)
            text_color = self._decide_color(currency[-1]) 
            self.currencyscr.addstr(self.content_y_start + i, x, f"{currency[0]} €", text_color) 
        
        self.currencyscr.noutrefresh()

    def chart_mode(self):

        self._add_titles()
        for i, currency in enumerate(self.currencies):
            code = currency[1] 
            currency_value = int(currency[2])
            code_and_value = f" {code} {currency_value} "
            chart_char = "|" 
            if len(chart_char * currency_value) + len(code_and_value) >= self.width - 6:
                chart_to_display = f"{chart_char * (self.width - len(code_and_value))}{code_and_value}"
            else:
                chart_to_display = f"{chart_char * currency_value}{code_and_value}"
            text_color = self._decide_color(currency[-1]) 
            self.currencyscr.addstr(self.content_y_start + i, 1, chart_to_display, text_color) 
        self.currencyscr.noutrefresh()


