import curses
from curses import wrapper
import requests
from currency_screen import Currencyscr
from currency_menu import Menu
from config import Config

class CurrencyApp:
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.frankfurter.app/latest?base=USD"
        self.base_dollar = True
        self.colors = []
        self.currencies_data = None
        self.screens = []
        self.menus = {}
        self.chart_mode = False
        
    def fetch_currencies(self, base_url):
        try:
            res = requests.get(base_url)
            res.raise_for_status()
            data = res.json()
            rates = data["rates"]

            continents = self.config.get_continents()
            result = {}
            for continent, currency_map in continents.items():
                result[continent] = [
                    [f"{name}: {rates[code]:.2f}", f"{code}", rates[code]]
                    for name, code in currency_map.items()
                    if code in rates
                ]
            return result
        except Exception:
            return None

    def get_colors(self):
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        
        magenta = curses.color_pair(1)
        green = curses.color_pair(2)
        red = curses.color_pair(3)
        
        return [red, magenta, green]

    def set_tui(self):
        self.colors = self.get_colors()
        dollar = "https://api.frankfurter.app/latest?base=USD" 
        euro = "https://api.frankfurter.app/latest" 

        self.base_url = dollar if self.base_dollar else euro
        self.currencies_data = self.fetch_currencies(self.base_url)
        
        if self.currencies_data is None:
            return False

        self.screens = [
            Currencyscr(self.currencies_data['asia'], "Asia", self.colors),
            Currencyscr(self.currencies_data['europe'], "Europe", self.colors),
            Currencyscr(self.currencies_data['america'], "America", self.colors),
            Currencyscr(self.currencies_data['oceania_africa'], "Oceania & Africa", self.colors)
        ]

        self.menus['title'] = Menu("[+] World Currencies  🌍", self.colors)
        self.menus['toggle_base'] = Menu("[+] d > To Toggle base $ | €", self.colors)
        self.menus['toggle_chart'] = Menu("[+] c > Toggle chart view", self.colors)
        self.menus['exit'] = Menu("[+] q > exit", self.colors)
        
        return True

    def draw_error(self, stdscr):
        import sys
        stdscr.erase()
        stdscr.box()
        stdscr.noutrefresh()

        height, width = stdscr.getmaxyx()
        error_menu = Menu("We've had an issue getting the data :(", self.colors)
        exit_menu = Menu("Press q to leave", self.colors)

        error_menu.make_menu_window(height // 2 - 2, (width - error_menu.ncols) // 2)
        exit_menu.make_menu_window(height - int(height * 0.3), 10)

        curses.doupdate()
        while stdscr.getch() != ord('q'):
            pass
        sys.exit()

    def draw_menus(self, height, width, screens_height):
        title_menu = self.menus['title']
        title_y = screens_height - int(0.8 * screens_height)
        title_x = (width - title_menu.ncols) // 2

        if title_y > 0 and title_x > 0:
            title_menu.make_menu_window(title_y, title_x)
            self.menus['toggle_chart'].make_menu_window(screens_height + int(0.6 * screens_height), 10)
            self.menus['toggle_base'].make_menu_window(screens_height + int(0.6 * screens_height), 40)
            self.menus['exit'].make_menu_window(screens_height + int(0.6 * screens_height), 75)

    def draw_all(self, stdscr):
        stdscr.erase()
        stdscr.box()

        height, width = stdscr.getmaxyx()
        screens_height = height // 2
        screens_width = width // 5
        screens_y = width // 14

        stdscr.noutrefresh()

        # Render continent screens at fixed intervals
        for i, screen in enumerate(self.screens):
            screen.make_screen(self.chart_mode, screens_height, screens_width, screens_y, screens_y * (1 + i * 3))

        self.draw_menus(height, width, screens_height)
        curses.doupdate()

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.timeout(-1)

        if not self.set_tui():
            self.draw_error(stdscr)

        while True:
            self.draw_all(stdscr)
            key = stdscr.getch()
            
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.chart_mode = not self.chart_mode
            elif key == ord('d'):
                self.base_dollar = not self.base_dollar
                wrapper(self.run)
                break
            elif key == curses.KEY_RESIZE:
                self.draw_all(stdscr)

if __name__ == '__main__':
    app = CurrencyApp()
    wrapper(app.run)
