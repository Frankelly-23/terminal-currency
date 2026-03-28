import curses

class Currencyscr:

    def __init__(self, currencies, title, colors ):
        self.currencies = currencies 
        self.title = title
        self.colors = colors

    def make_screen(self, char_mode, nlines, ncols, beginY, beginX):
        self.currencyscr = curses.newwin(nlines, ncols, beginY, beginX)
        
        self.height, self.width = self.currencyscr.getmaxyx()
        self.title_x = max(0, (self.width - len(self.title)) // 2)
        self.title_y = self.height // 5
        self.content_y_start = self.title_y + 2

        self.currencyscr.erase()
        self.currencyscr.addstr(self.title_y, self.title_x, self.title)

        self.currencyscr.box()

        if char_mode: 
            self.chart_mode()
        else:
            self.write_currency()

    def _decide_color(self, value):
        low = 20
        medium = 100
        # RED MAGENTA GREEN 
        if value < low:
            return self.colors[0]
        elif value < medium:
           return self.colors[1]
        else:
            return self.colors[2]


    def write_currency(self):

        # Draw currencies
        for i, currency in enumerate(self.currencies):
            if self.content_y_start + i >= self.height - 1:
                break
            x = max(0, (self.width - len(currency[0])) // 2)
            text_color = self._decide_color(currency[-1]) 
            self.currencyscr.addstr(self.content_y_start + i, x, f"{currency[0]} ", text_color) 
        
        self.currencyscr.noutrefresh()

    def chart_mode(self):

        values = [c[2] for c in self.currencies] 
        max_val = max(values) 
        
        for i, currency in enumerate(self.currencies):
            if self.content_y_start + i >= self.height - 1:
                break
                
            code = currency[1] 
            val = currency[2]

            label = f" {code} {val:.2f} "
            
            available_width = self.width - len(label) - 4
            
            num_bars = int((val / max_val) * available_width) if max_val > 0 else 0
            
            chart_char = "|" 
            chart_to_display = f"{chart_char * num_bars}{label}"
            
            text_color = self._decide_color(val) 
            self.currencyscr.addstr(self.content_y_start + i, 2, chart_to_display, text_color) 
            
        self.currencyscr.noutrefresh()


