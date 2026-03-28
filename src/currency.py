
import curses
from curses import wrapper
from currency_screen import Currencyscr 
from currency_menu import Menu
from config import Config
import requests

config = Config()

def get_Currencies():
    try:
        res = requests.get("https://api.frankfurter.app/latest")
        res.raise_for_status()
        data = res.json()
        rates = data["rates"] 

        continents = config.get_continents()

        result  = {}
        for continent, currency_map in continents.items():
            result[continent] = [[f"{name}: {rates[code]:.2f}", f"{code}", rates[code]] for name, code in currency_map.items() if code in rates]

        return result

    except Exception:
        return None


def draw_error(color, stdscr):

    stdscr.erase()
    stdscr.box()
    height, width = stdscr.getmaxyx()
    error_message = "We've had an issue getting the data :("
    exit_message = "Press any key to leave"
    
    mid_y, mid_x = height // 2, width // 2
    
    stdscr.addstr(mid_y, mid_x - len(error_message)//2, error_message, color[1])
    stdscr.addstr(mid_y + 2, mid_x - len(exit_message)//2, exit_message, color[0])
    
    stdscr.refresh()
    stdscr.getch()

def get_colors():
    # colors
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) 
    MAGENTA = curses.color_pair(1)
    GREEN  = curses.color_pair(2)
    RED = curses.color_pair(3)
    
    return [MAGENTA, GREEN, RED]

def main(stdscr):

    colors = get_colors() 
    currencies_per_continent = get_Currencies()

    if currencies_per_continent is None:
       draw_error(colors, stdscr) 
       return

    curses.curs_set(0)  
    
    asia_scr = Currencyscr(
            currencies_per_continent['asia'], 
            "Asia", 
            colors
            ) 
    europe_scr = Currencyscr(
            currencies_per_continent['europe'], 
            "Europe", 
            colors
            ) 
    america_scr = Currencyscr(
        currencies_per_continent['america'] , 
            "America", 
            colors
            )
    ocenia_and_africa_scr = Currencyscr(
            currencies_per_continent['oceania_africa'], 
            "Oceania & Africa", 
            colors 
            ) 

    
    # If dynamic updates are added later.
    stdscr.timeout(-1)

    title_menu = Menu("World Currencies  🌍", colors, 5, 73)
    toggle_chart_menu = Menu("[+] c | Toggle chart view", colors, 30, 10) 
    exit_menu = Menu("[+] q | exit", colors, 30, 40) 

    def draw_all(isChartMode):

        #Main Screen
        stdscr.erase()
        stdscr.box()
        
        height, width = stdscr.getmaxyx()

        screens_height = height // 2
        screens_width = width // 5 
        screens_y = width // 14 # will begin at y ~ 10 on my terminal
        
        stdscr.noutrefresh()

        asia_scr.make_screen(isChartMode, screens_height, screens_width , screens_y, screens_y * 1)
        europe_scr.make_screen(isChartMode, screens_height, screens_width, screens_y, screens_y * 4)
        america_scr.make_screen(isChartMode, screens_height, screens_width, screens_y, screens_y * 7)
        ocenia_and_africa_scr.make_screen(isChartMode, screens_height, screens_width, screens_y, screens_y * 10)


        toggle_chart_menu.draw_menu()  
        exit_menu.draw_menu()
        title_menu.draw_menu() 

        curses.doupdate()

    chartMode = False 

    while True:
        draw_all(chartMode)
        # Check for user input (q to quit)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('c'):
            chartMode = not chartMode
        elif key == curses.KEY_RESIZE:
            draw_all(chartMode)

if __name__ == '__main__':
    wrapper(main)
