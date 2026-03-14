import curses

class Currencyscr:
    def __init__(self, currencies: list[str], title: str, nlines: int, ncols: int, beginY: int, beginX: int, color: int):
        self.currencies: list[str] = currencies 
        self.title: str = title
        self.color: int = color
        self.currencyscr: curses.window = curses.newwin(nlines, ncols, beginY, beginX)
        
        self.height, self.width = self.currencyscr.getmaxyx()
        self.title_x: int = max(0, (self.width - len(self.title)) // 2)
        self.title_y: int = self.height // 5
        self.content_y_start: int = self.title_y + 2

    def write_currency(self):
        self.currencyscr.erase()
        self.currencyscr.box()
        
        self.currencyscr.addstr(self.title_y, self.title_x, self.title, self.color)

        # Draw currencies
        for i, currency in enumerate(self.currencies):
            if self.content_y_start + i >= self.height - 1:
                break
            x = max(0, (self.width - len(currency)) // 2)
            self.currencyscr.addstr(self.content_y_start + i, x, f"{currency} €") 
        
        self.currencyscr.noutrefresh()

